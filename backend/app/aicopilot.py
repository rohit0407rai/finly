from groq import Groq
from sqlalchemy.orm import Session
from app.models import Expense, User
from datetime import datetime, date
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# S — sirf data fetch karna
def get_user_expense_summary(db: Session, user_id: str) -> dict:
    expenses = db.query(Expense).filter(
        Expense.user_id == user_id
    ).all()

    if not expenses:
        return {"total": 0, "expenses": [], "by_category": {}}

    # Category wise total
    by_category = {}
    for exp in expenses:
        cat = exp.category
        if cat not in by_category:
            by_category[cat] = 0
        by_category[cat] += float(exp.amount)

    # Expense list for AI
    expense_list = [
        {
            "amount": float(exp.amount),
            "category": exp.category,
            "description": exp.description,
            "date": str(exp.date)
        }
        for exp in expenses
    ]

    return {
        "total": sum(e["amount"] for e in expense_list),
        "count": len(expense_list),
        "by_category": by_category,
        "expenses": expense_list
    }


# S — sirf AI call karna
def ask_ai(question: str, expense_data: dict, user_name: str) -> str:
    system_prompt = f"""You are Finly, a personal finance assistant for {user_name}.
You have access to their expense data. Answer in a friendly, concise way.
Always respond in the same language the user asks in.
If they ask in English, respond in English.

Current date: {date.today()}

User's expense summary:
- Total spent: ₹{expense_data['total']}
- Total transactions: {expense_data['count']}
- By category: {expense_data['by_category']}
- All expenses: {expense_data['expenses']}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        max_tokens=500,
        temperature=0.7
    )

    return response.choices[0].message.content