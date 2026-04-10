from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserRegister, UserLogin, UserResponse, Token
from app.auth import hash_password, verify_password, create_access_token
from datetime import timedelta
import os

router = APIRouter(prefix="/auth", tags=["Auth"])


# S — sirf registration ka kaam
@router.post("/register", response_model=UserResponse)
def register(payload: UserRegister, db: Session = Depends(get_db)):

    # Email already exist karta hai?
    existing_user = db.query(User).filter(
        User.email == payload.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Password hash karo
    hashed = hash_password(payload.password)

    # User banao
    new_user = User(
        name=payload.name,
        email=payload.email,
        password_hash=hashed
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# S — sirf login ka kaam
@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):

    # User dhundho
    user = db.query(User).filter(
        User.email == payload.email
    ).first()

    # User nahi mila ya password wrong
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Token banao
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(
            minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
        )
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }