from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.database import get_db
from app.models import Expense
from app.schemas import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from app.auth import get_current_user
from app.models import User

router = APIRouter(prefix="/expenses", tags=["Expenses"])


# GET — sabke expenses (sirf apne)
@router.get("/", response_model=List[ExpenseResponse])
def get_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Expense).filter(
        Expense.user_id == current_user.id
    ).all()


# POST — naya expense add karo
@router.post("/", response_model=ExpenseResponse)
def create_expense(
    payload: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_expense = Expense(
        user_id=current_user.id,
        amount=payload.amount,
        category=payload.category,
        description=payload.description,
        date=payload.date
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


# GET — ek specific expense
@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id  # sirf apna dekh sakta hai
    ).first()

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    return expense


# PUT — expense update karo
@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: UUID,
    payload: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    # Sirf jo fields aaye hain unhe update karo
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(expense, field, value)

    db.commit()
    db.refresh(expense)

    return expense


# DELETE — expense delete karo
@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    db.delete(expense)
    db.commit()