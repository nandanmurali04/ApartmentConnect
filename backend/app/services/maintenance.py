from sqlalchemy.orm import Session

from app.models.maintenance import Maintenance
from app.models.flat import Flat


def create_maintenance(
    db: Session,
    maintenance_data,
):
    flat = (
        db.query(Flat)
        .filter(Flat.id == maintenance_data.flat_id)
        .first()
    )

    if flat is None:
        return None

    maintenance = Maintenance(
        flat_id=maintenance_data.flat_id,
        month=maintenance_data.month,
        year=maintenance_data.year,
        amount=maintenance_data.amount,
        due_date=maintenance_data.due_date,
    )

    db.add(maintenance)
    db.commit()
    db.refresh(maintenance)

    return maintenance


def get_all_maintenance(db: Session):
    return db.query(Maintenance).all()