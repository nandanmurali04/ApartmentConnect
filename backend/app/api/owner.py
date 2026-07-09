from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.owner import (
    OwnerCreate,
    OwnerUpdate,
    OwnerResponse,
)

from app.services.owner import (
    create_owner,
    get_all_owners,
    update_owner,
    delete_owner,
)

router = APIRouter(
    prefix="/owners",
    tags=["Owners"],
)


@router.post("/", response_model=OwnerResponse)
def add_owner(
    owner: OwnerCreate,
    db: Session = Depends(get_db),
):
    created = create_owner(
        db=db,
        owner_data=owner,
    )

    if created is None:
        raise HTTPException(
            status_code=404,
            detail="Flat not found",
        )

    return created


@router.get("/", response_model=list[OwnerResponse])
def list_owners(
    db: Session = Depends(get_db),
):
    return get_all_owners(db)


@router.put("/{owner_id}", response_model=OwnerResponse)
def edit_owner(
    owner_id: int,
    owner: OwnerUpdate,
    db: Session = Depends(get_db),
):
    updated = update_owner(
        db=db,
        owner_id=owner_id,
        owner_data=owner,
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Owner or Flat not found",
        )

    return updated
@router.delete("/{owner_id}")
def remove_owner(
    owner_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_owner(
        db=db,
        owner_id=owner_id,
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Owner not found",
        )

    return {
        "message": "Owner deleted successfully"
    }