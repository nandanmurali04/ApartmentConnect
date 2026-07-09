from pydantic import BaseModel


class FlatCreate(BaseModel):
    flat_number: str
    block: str
    floor: int
    flat_type: str
    maintenance_amount: int
    is_occupied: bool = False


class FlatUpdate(BaseModel):
    flat_number: str
    block: str
    floor: int
    flat_type: str
    maintenance_amount: int
    is_occupied: bool


class FlatResponse(FlatCreate):
    id: int

    class Config:
        from_attributes = True