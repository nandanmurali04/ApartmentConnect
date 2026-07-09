from pydantic import BaseModel
from datetime import date


# -----------------------------
# Create Maintenance
# -----------------------------
class MaintenanceCreate(BaseModel):
    flat_id: int
    month: str
    year: int
    amount: float
    due_date: date


# -----------------------------
# Generate Bills
# -----------------------------
class GenerateBillsRequest(BaseModel):
    month: str
    year: int
    due_date: date


# -----------------------------
# Maintenance Response
# -----------------------------
class MaintenanceResponse(BaseModel):
    id: int

    flat_id: int
    flat_number: str
    block: str

    month: str
    year: int
    amount: float
    status: str
    due_date: date

    class Config:
        from_attributes = True