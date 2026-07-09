from pydantic import BaseModel, EmailStr


class OwnerCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    flat_id: int


class OwnerUpdate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    flat_id: int


class OwnerResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str

    flat_id: int
    flat_number: str
    block: str

    class Config:
        from_attributes = True