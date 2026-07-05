from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.flat import FlatCreate, FlatResponse
from app.services.flat import create_flat, get_all_flats

router = APIRouter(
    prefix="/flats",
    tags=["Flats"],
)


@router.post("/", response_model=FlatResponse)
def add_flat(
    flat: FlatCreate,
    db: Session = Depends(get_db),
):
    return create_flat(db, flat)


@router.get("/", response_model=list[FlatResponse])
def list_flats(
    db: Session = Depends(get_db),
):
    return get_all_flats(db)