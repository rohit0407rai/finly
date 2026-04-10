from pydantic import BaseModel, EmailStr
from datetime import date as DateType
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from typing import Optional


# I — Interface Segregation
# Alag alag use case ke liye alag alag schema
# Ek bada schema nahi banaya

# ─── AUTH SCHEMAS ───────────────────────────────

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Response me password kabhi nahi jayega
class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True  # SQLAlchemy model → Pydantic schema


# ─── TOKEN SCHEMAS ──────────────────────────────

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str] = None


# ─── EXPENSE SCHEMAS ────────────────────────────

class ExpenseCreate(BaseModel):
    amount: Decimal
    category: str
    description: Optional[str] = None
    date: Optional[DateType] = None


class ExpenseUpdate(BaseModel):
    amount: Optional[Decimal] = None
    category: Optional[str] = None
    description: Optional[str] = None
    date: Optional[DateType] = None


class ExpenseResponse(BaseModel):
    id: UUID
    user_id: UUID
    amount: Decimal
    category: str
    description: Optional[str]
    date: DateType
    created_at: datetime

    class Config:
        from_attributes = True