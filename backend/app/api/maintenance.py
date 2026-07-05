from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.maintenance import (
    MaintenanceCreate,
    MaintenanceResponse,
)
from app.services.maintenance import (
    create_maintenance,
    get_all_maintenance,
)

router = APIRouter(
    prefix="/maintenance",
    tags=["Maintenance"],
)


@router.post("/", response_model=MaintenanceResponse)
def add_maintenance(
    maintenance: MaintenanceCreate,
    db: Session = Depends(get_db),
):
    record = create_maintenance(db, maintenance)

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Flat not found",
        )

    return record


@router.get("/", response_model=list[MaintenanceResponse])
def list_maintenance(
    db: Session = Depends(get_db),
):
    return get_all_maintenance(db)