from sqlalchemy.orm import Session

from app.models.owner import Owner
from app.models.flat import Flat


def create_owner(db: Session, owner_data):
    flat = (
        db.query(Flat)
        .filter(Flat.id == owner_data.flat_id)
        .first()
    )

    if flat is None:
        return None

    owner = Owner(
        full_name=owner_data.full_name,
        email=owner_data.email,
        phone=owner_data.phone,
        flat_id=owner_data.flat_id,
    )

    flat.is_occupied = True

    db.add(owner)
    db.commit()
    db.refresh(owner)

    return owner


def get_all_owners(db: Session):
    return db.query(Owner).all()