from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base


class Flat(Base):
    __tablename__ = "flats"

    id = Column(Integer, primary_key=True, index=True)

    flat_number = Column(String, unique=True, nullable=False)

    block = Column(String, nullable=False)

    floor = Column(Integer, nullable=False)

    is_occupied = Column(Boolean, default=False)