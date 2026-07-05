from datetime import date
from pydantic import BaseModel


class MaintenanceCreate(BaseModel):
    flat_id: int
    month: str
    year: int
    amount: float
    due_date: date


class MaintenanceResponse(MaintenanceCreate):
    id: int
    status: str

    class Config:
        from_attributes = True