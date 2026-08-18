from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    name: str
    phone_number: str | None = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    name: str
    phone_number: str | None = None
    role: str

    model_config = {
        "from_attributes": True
    }


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    name: str | None = None
    phone_number: str | None = None
