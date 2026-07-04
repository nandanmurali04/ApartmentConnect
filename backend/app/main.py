from fastapi import FastAPI
from sqlalchemy import text

from app.db.database import engine, Base
from app.models.user import User

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ApartmentConnect API",
    description="Apartment Association Management System",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to ApartmentConnect 🚀"
    }


@app.get("/db-test")
def db_test():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {
        "message": "Database connected successfully!"
    }