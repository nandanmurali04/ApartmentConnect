from fastapi import FastAPI
from sqlalchemy import text

from app.db.database import engine, Base
from app.models.user import User
from app.api.auth import router as auth_router
from app.models.flat import Flat
from app.api.flat import router as flat_router
from app.models.owner import Owner
from app.api.owner import router as owner_router
from app.models.maintenance import Maintenance
from app.api.maintenance import router as maintenance_router

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ApartmentConnect API",
    description="Apartment Association Management System",
    version="1.0.0"
)
app.include_router(auth_router)
app.include_router(flat_router)
app.include_router(owner_router)
app.include_router(maintenance_router)

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