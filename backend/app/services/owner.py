from sqlalchemy.orm import Session, joinedload

from app.models.owner import Owner
from app.models.flat import Flat


def create_owner(
    db: Session,
    owner_data,
):
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

    db.add(owner)

    flat.is_occupied = True

    db.commit()
    db.refresh(owner)

    return owner


def get_all_owners(db: Session):

    owners = (
        db.query(Owner)
        .options(joinedload(Owner.flat))
        .all()
    )

    result = []

    for owner in owners:

        result.append({
            "id": owner.id,
            "full_name": owner.full_name,
            "email": owner.email,
            "phone": owner.phone,
            "flat_id": owner.flat_id,
            "flat_number": owner.flat.flat_number,
            "block": owner.flat.block,
        })

    return result


def update_owner(
    db: Session,
    owner_id: int,
    owner_data,
):
    owner = (
        db.query(Owner)
        .filter(Owner.id == owner_id)
        .first()
    )

    if owner is None:
        return None

    flat = (
        db.query(Flat)
        .filter(Flat.id == owner_data.flat_id)
        .first()
    )

    if flat is None:
        return None

    owner.full_name = owner_data.full_name
    owner.email = owner_data.email
    owner.phone = owner_data.phone
    owner.flat_id = owner_data.flat_id

    flat.is_occupied = True

    db.commit()
    db.refresh(owner)

    return owner


def delete_owner(
    db: Session,
    owner_id: int,
):
    owner = (
        db.query(Owner)
        .filter(Owner.id == owner_id)
        .first()
    )

    if owner is None:
        return None

    flat = (
        db.query(Flat)
        .filter(Flat.id == owner.flat_id)
        .first()
    )

    if flat:
        flat.is_occupied = False

    db.delete(owner)

    db.commit()

    return True