from sqlalchemy.orm import Session

from app.models.flat import Flat


def create_flat(db: Session, flat_data):

    flat = Flat(
        flat_number=flat_data.flat_number,
        block=flat_data.block,
        floor=flat_data.floor,
        flat_type=flat_data.flat_type,
        maintenance_amount=flat_data.maintenance_amount,
        is_occupied=flat_data.is_occupied,
    )

    db.add(flat)
    db.commit()
    db.refresh(flat)

    return flat


def get_all_flats(db: Session):

    return db.query(Flat).all()


# NEW
def get_vacant_flats(db: Session):

    return (
        db.query(Flat)
        .filter(Flat.is_occupied == False)
        .all()
    )


def update_flat(
    db: Session,
    flat_id: int,
    flat_data,
):

    flat = (
        db.query(Flat)
        .filter(Flat.id == flat_id)
        .first()
    )

    if flat is None:
        return None

    flat.flat_number = flat_data.flat_number
    flat.block = flat_data.block
    flat.floor = flat_data.floor
    flat.flat_type = flat_data.flat_type
    flat.maintenance_amount = flat_data.maintenance_amount
    flat.is_occupied = flat_data.is_occupied

    db.commit()
    db.refresh(flat)

    return flat


def delete_flat(
    db: Session,
    flat_id: int,
):

    flat = (
        db.query(Flat)
        .filter(Flat.id == flat_id)
        .first()
    )

    if flat is None:
        return None

    db.delete(flat)

    db.commit()

    return True