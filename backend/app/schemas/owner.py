from pydantic import BaseModel


class OwnerCreate(BaseModel):
    full_name: str
    email: str
    phone: str
    flat_id: int


class OwnerResponse(OwnerCreate):
    id: int

    class Config:
        from_attributes = True