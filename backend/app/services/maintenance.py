from datetime import date

from sqlalchemy.orm import Session

from app.models.maintenance import Maintenance
from app.models.flat import Flat
from app.models.owner import Owner
from app.utils.email import send_email


# -----------------------------
# Update Pending -> Overdue
# -----------------------------
def update_overdue_status(db: Session):

    today = date.today()

    records = (
        db.query(Maintenance)
        .filter(Maintenance.status == "Pending")
        .all()
    )

    for record in records:

        if record.due_date < today:
            record.status = "Overdue"

    db.commit()


# -----------------------------
# Create Maintenance
# -----------------------------
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


# -----------------------------
# Get All Maintenance
# -----------------------------
def get_all_maintenance(db: Session):

    update_overdue_status(db)

    records = (
        db.query(Maintenance, Flat)
        .join(Flat, Maintenance.flat_id == Flat.id)
        .all()
    )

    result = []

    for maintenance, flat in records:

        result.append({
            "id": maintenance.id,

            "flat_id": flat.id,
            "flat_number": flat.flat_number,
            "block": flat.block,

            "month": maintenance.month,
            "year": maintenance.year,
            "amount": maintenance.amount,
            "status": maintenance.status,
            "due_date": maintenance.due_date,
        })

    return result

# -----------------------------
# Mark Maintenance Paid
# -----------------------------
def mark_as_paid(
    db: Session,
    maintenance_id: int,
):
    maintenance = (
        db.query(Maintenance)
        .filter(Maintenance.id == maintenance_id)
        .first()
    )

    if maintenance is None:
        return None

    maintenance.status = "Paid"

    db.commit()
    db.refresh(maintenance)

    return maintenance


# -----------------------------
# Generate Monthly Bills
# -----------------------------
def generate_monthly_bills(
    db: Session,
    month: str,
    year: int,
    due_date,
):
    flats = (
        db.query(Flat)
        .filter(Flat.is_occupied == True)
        .all()
    )

    created = 0

    for flat in flats:

        existing = (
            db.query(Maintenance)
            .filter(
                Maintenance.flat_id == flat.id,
                Maintenance.month == month,
                Maintenance.year == year,
            )
            .first()
        )

        if existing:
            continue

        bill = Maintenance(
            flat_id=flat.id,
            month=month,
            year=year,
            amount=flat.maintenance_amount,
            due_date=due_date,
            status="Pending",
        )

        db.add(bill)
        created += 1

    db.commit()

    return created


# -----------------------------
# Pending Maintenance
# -----------------------------
def get_pending_maintenance(db: Session):

    update_overdue_status(db)

    records = (
        db.query(Maintenance, Flat, Owner)
        .join(Flat, Maintenance.flat_id == Flat.id)
        .join(Owner, Owner.flat_id == Flat.id)
        .filter(Maintenance.status == "Pending")
        .all()
    )

    result = []

    for maintenance, flat, owner in records:

        result.append({
            "flat_number": flat.flat_number,
            "owner_name": owner.full_name,
            "email": owner.email,
            "phone": owner.phone,
            "month": maintenance.month,
            "year": maintenance.year,
            "amount": maintenance.amount,
            "due_date": maintenance.due_date,
        })

    return result


# -----------------------------
# Send One Reminder
# -----------------------------
def send_maintenance_reminder(
    db: Session,
    maintenance_id: int,
):
    update_overdue_status(db)

    record = (
        db.query(Maintenance)
        .filter(Maintenance.id == maintenance_id)
        .first()
    )

    if not record:
        return None

    flat = (
        db.query(Flat)
        .filter(Flat.id == record.flat_id)
        .first()
    )

    owner = (
        db.query(Owner)
        .filter(Owner.flat_id == flat.id)
        .first()
    )

    if owner is None:
        return None

    subject = f"Maintenance Reminder - {record.month} {record.year}"

    if record.status == "Overdue":
        message = "This is a reminder that your apartment maintenance payment is OVERDUE."
    else:
        message = "This is a reminder that your apartment maintenance payment is still pending."

    body = f"""
Dear {owner.full_name},

{message}

Flat Number : {flat.flat_number}
Month       : {record.month}
Year        : {record.year}
Amount      : ₹{int(record.amount)}
Due Date    : {record.due_date}
Status      : {record.status}

Kindly make the payment at the earliest.

Thank you,
Apartment Association
"""

    send_email(
        owner.email,
        subject,
        body,
    )

    return True


# -----------------------------
# Send Reminders to ALL Overdue Owners
# -----------------------------
def send_all_overdue_reminders(db: Session):

    update_overdue_status(db)

    overdue_records = (
        db.query(Maintenance)
        .filter(Maintenance.status == "Overdue")
        .all()
    )

    sent = 0

    for record in overdue_records:

        flat = (
            db.query(Flat)
            .filter(Flat.id == record.flat_id)
            .first()
        )

        owner = (
            db.query(Owner)
            .filter(Owner.flat_id == flat.id)
            .first()
        )

        if owner is None:
            continue

        subject = f"Maintenance Reminder - {record.month} {record.year}"

        body = f"""
Dear {owner.full_name},

This is a reminder that your apartment maintenance payment is OVERDUE.

Flat Number : {flat.flat_number}
Month       : {record.month}
Year        : {record.year}
Amount      : ₹{int(record.amount)}
Due Date    : {record.due_date}
Status      : {record.status}

Kindly make the payment as soon as possible.

Thank you,
Apartment Association
"""

        send_email(
            owner.email,
            subject,
            body,
        )

        sent += 1

    return sent


# -----------------------------
# Excel Report
# -----------------------------
def get_maintenance_report(db: Session):

    update_overdue_status(db)

    records = (
        db.query(Maintenance, Flat, Owner)
        .join(Flat, Maintenance.flat_id == Flat.id)
        .join(Owner, Owner.flat_id == Flat.id)
        .all()
    )

    report = []

    for maintenance, flat, owner in records:

        report.append({
            "flat_number": flat.flat_number,
            "owner_name": owner.full_name,
            "email": owner.email,
            "phone": owner.phone,
            "month": maintenance.month,
            "year": maintenance.year,
            "amount": maintenance.amount,
            "status": maintenance.status,
            "due_date": maintenance.due_date,
        })

    return report