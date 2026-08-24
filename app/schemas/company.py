from datetime import datetime

from pydantic import BaseModel, HttpUrl


class CompanyCreate(BaseModel):
    name: str
    description: str | None = None
    website: HttpUrl | None = None
    location: str | None = None
    logo: HttpUrl | None = None


class CompanyResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    website: HttpUrl | None = None
    location: str | None = None
    logo: HttpUrl | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


class CompanyUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    website: HttpUrl | None = None
    location: str | None = None
    logo: HttpUrl | None = None
