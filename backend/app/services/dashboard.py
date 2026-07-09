from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.flat import Flat
from app.models.owner import Owner
from app.models.maintenance import Maintenance


def get_dashboard_stats(db: Session):
    total_flats = db.query(Flat).count()

    occupied_flats = (
        db.query(Flat)
        .filter(Flat.is_occupied == True)
        .count()
    )

    vacant_flats = (
        db.query(Flat)
        .filter(Flat.is_occupied == False)
        .count()
    )

    total_owners = db.query(Owner).count()

    pending = (
        db.query(Maintenance)
        .filter(Maintenance.status == "Pending")
        .count()
    )

    paid = (
        db.query(Maintenance)
        .filter(Maintenance.status == "Paid")
        .count()
    )

    total_collection = (
        db.query(func.sum(Maintenance.amount))
        .filter(Maintenance.status == "Paid")
        .scalar()
        or 0
    )

    return {
        "total_flats": total_flats,
        "occupied_flats": occupied_flats,
        "vacant_flats": vacant_flats,
        "total_owners": total_owners,
        "pending_maintenance": pending,
        "paid_maintenance": paid,
        "total_collection": total_collection,
    }