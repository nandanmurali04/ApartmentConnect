from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.flat import (
    FlatCreate,
    FlatUpdate,
    FlatResponse,
)

from app.services.flat import (
    create_flat,
    get_all_flats,
    get_vacant_flats,
    update_flat,
    delete_flat,
)

router = APIRouter(
    prefix="/flats",
    tags=["Flats"],
)


# -------------------------
# Add Flat
# -------------------------
@router.post("/", response_model=FlatResponse)
def add_flat(
    flat: FlatCreate,
    db: Session = Depends(get_db),
):
    return create_flat(db, flat)


# -------------------------
# List All Flats
# -------------------------
@router.get("/", response_model=list[FlatResponse])
def list_flats(
    db: Session = Depends(get_db),
):
    return get_all_flats(db)


# -------------------------
# List Vacant Flats
# -------------------------
@router.get("/vacant", response_model=list[FlatResponse])
def list_vacant_flats(
    db: Session = Depends(get_db),
):
    return get_vacant_flats(db)


# -------------------------
# Update Flat
# -------------------------
@router.put("/{flat_id}", response_model=FlatResponse)
def edit_flat(
    flat_id: int,
    flat: FlatUpdate,
    db: Session = Depends(get_db),
):
    updated = update_flat(
        db=db,
        flat_id=flat_id,
        flat_data=flat,
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Flat not found",
        )

    return updated


# -------------------------
# Delete Flat
# -------------------------
@router.delete("/{flat_id}")
def remove_flat(
    flat_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_flat(
        db=db,
        flat_id=flat_id,
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Flat not found",
        )

    return {
        "message": "Flat deleted successfully"
    }