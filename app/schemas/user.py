from pydantic import BaseModel, EmailStr, Field, field_validator
from app.core.security import validate_password


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    name: str = Field(min_length=2, max_length=100)
    phone_number: str | None = Field(default=None, max_length=20)

    _validate_password = field_validator("password")(validate_password)


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
