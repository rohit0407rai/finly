from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# S — sirf connection string yahan hai
DATABASE_URL = os.getenv("DATABASE_URL")

# Engine = PostgreSQL se baat karne wala object
engine = create_engine(DATABASE_URL)

# SessionLocal = har request ke liye ek DB session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = saare models isse inherit karenge
Base = declarative_base()


# D — Dependency Injection
# Ye function FastAPI routes ko DB session deta hai
# Route directly session nahi banata — yahan se leta hai
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()