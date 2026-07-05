from pydantic import BaseModel


class FlatCreate(BaseModel):
    flat_number: str
    block: str
    floor: int
    is_occupied: bool = False


class FlatResponse(FlatCreate):
    id: int

    class Config:
        from_attributes = True