from sqlalchemy import Column, Integer, Float, String, Date, DateTime, ForeignKey
from datetime import datetime

from app.db.database import Base


class Maintenance(Base):
    __tablename__ = "maintenance"

    id = Column(Integer, primary_key=True, index=True)

    flat_id = Column(
        Integer,
        ForeignKey("flats.id"),
        nullable=False,
    )

    month = Column(String, nullable=False)

    year = Column(Integer, nullable=False)

    amount = Column(Float, nullable=False)

    due_date = Column(Date, nullable=False)

    status = Column(
        String,
        default="Pending",
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )