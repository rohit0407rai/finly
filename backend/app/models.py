import uuid
from sqlalchemy import Column, String, Numeric, Text, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


# S — User table ki sirf apni class hai
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    password_hash = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationship — ek user ke multiple expenses ho sakte hain
    expenses = relationship("Expense", back_populates="user", cascade="all, delete")


# S — Expense table ki sirf apni class hai
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    date = Column(Date, server_default=func.current_date())
    created_at = Column(DateTime, server_default=func.now())

    # Relationship — expense ka owner user hai
    user = relationship("User", back_populates="expenses")