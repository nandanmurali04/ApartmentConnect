from sqlalchemy.orm import Session

from app.models.flat import Flat


def create_flat(db: Session, flat_data):
    flat = Flat(
        flat_number=flat_data.flat_number,
        block=flat_data.block,
        floor=flat_data.floor,
        is_occupied=flat_data.is_occupied,
    )

    db.add(flat)
    db.commit()
    db.refresh(flat)

    return flat


def get_all_flats(db: Session):
    return db.query(Flat).all()