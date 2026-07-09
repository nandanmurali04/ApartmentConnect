from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.maintenance import (
    MaintenanceCreate,
    MaintenanceResponse,
    GenerateBillsRequest,
)

from app.services.maintenance import (
    create_maintenance,
    get_all_maintenance,
    mark_as_paid,
    generate_monthly_bills,
    get_pending_maintenance,
    send_maintenance_reminder,
    send_all_overdue_reminders,
    get_maintenance_report,
)

from app.utils.excel import create_maintenance_excel

router = APIRouter(
    prefix="/maintenance",
    tags=["Maintenance"],
)


# -------------------------
# Add Maintenance
# -------------------------
@router.post("/", response_model=MaintenanceResponse)
def add_maintenance(
    maintenance: MaintenanceCreate,
    db: Session = Depends(get_db),
):
    record = create_maintenance(db, maintenance)

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Flat not found",
        )

    return record


# -------------------------
# Generate Monthly Bills
# -------------------------
@router.post("/generate")
def generate_bills(
    request: GenerateBillsRequest,
    db: Session = Depends(get_db),
):
    created = generate_monthly_bills(
        db=db,
        month=request.month,
        year=request.year,
        due_date=request.due_date,
    )

    return {
        "message": f"{created} maintenance bills generated successfully."
    }


# -------------------------
# List All Maintenance
# -------------------------
@router.get("/", response_model=list[MaintenanceResponse])
def list_maintenance(
    db: Session = Depends(get_db),
):
    return get_all_maintenance(db)


# -------------------------
# Pending Maintenance
# -------------------------
@router.get("/pending")
def pending_maintenance(
    db: Session = Depends(get_db),
):
    return get_pending_maintenance(db)


# -------------------------
# Mark as Paid
# -------------------------
@router.put("/{maintenance_id}/paid")
def pay_maintenance(
    maintenance_id: int,
    db: Session = Depends(get_db),
):
    maintenance = mark_as_paid(
        db,
        maintenance_id,
    )

    if maintenance is None:
        raise HTTPException(
            status_code=404,
            detail="Maintenance record not found",
        )

    return {
        "message": "Maintenance marked as Paid"
    }


# -------------------------
# Send Reminder to One Owner
# -------------------------
@router.post("/{maintenance_id}/reminder")
def send_reminder(
    maintenance_id: int,
    db: Session = Depends(get_db),
):
    success = send_maintenance_reminder(
        db=db,
        maintenance_id=maintenance_id,
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Unable to send reminder",
        )

    return {
        "message": "Reminder email sent successfully"
    }


# -------------------------
# Send Reminder to All Overdue Owners
# -------------------------
@router.post("/send-overdue-reminders")
def send_all_reminders(
    db: Session = Depends(get_db),
):
    total = send_all_overdue_reminders(db)

    return {
        "message": f"{total} overdue reminder emails sent successfully."
    }


# -------------------------
# Export Maintenance Report
# -------------------------
@router.get("/export")
def export_maintenance(
    db: Session = Depends(get_db),
):
    report = get_maintenance_report(db)

    file_name = create_maintenance_excel(report)

    return FileResponse(
        path=file_name,
        filename=file_name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )