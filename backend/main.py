import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import auth, expenses

# Tables automatically create karo agar exist nahi karti
Base.metadata.create_all(bind=engine)
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app = FastAPI(
    title="Finly API",
    description="AI-powered personal finance OS",
    version="1.0.0"
)

# CORS — frontend se requests allow karo
app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,  # Next.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers register karo
app.include_router(auth.router)
app.include_router(expenses.router)


@app.get("/")
def root():
    return {"message": "Finly API is running 🚀"}