from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.owner import OwnerCreate, OwnerResponse
from app.services.owner import create_owner, get_all_owners

router = APIRouter(
    prefix="/owners",
    tags=["Owners"],
)


@router.post("/", response_model=OwnerResponse)
def add_owner(
    owner: OwnerCreate,
    db: Session = Depends(get_db),
):
    new_owner = create_owner(db, owner)

    if new_owner is None:
        raise HTTPException(
            status_code=404,
            detail="Flat not found"
        )

    return new_owner


@router.get("/", response_model=list[OwnerResponse])
def list_owners(
    db: Session = Depends(get_db),
):
    return get_all_owners(db)