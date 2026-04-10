from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import User
from app.auth import get_current_user
from app.aicopilot import get_user_expense_summary, ask_ai

router = APIRouter(prefix="/ai", tags=["AI Copilot"])


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str


@router.post("/ask", response_model=AskResponse)
def ask_copilot(
    payload: AskRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # User ka expense data fetch karo
    expense_data = get_user_expense_summary(
        db=db,
        user_id=str(current_user.id)
    )

    # AI se answer lo
    answer = ask_ai(
        question=payload.question,
        expense_data=expense_data,
        user_name=current_user.name
    )

    return {"answer": answer}