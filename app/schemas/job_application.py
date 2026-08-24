from datetime import datetime

from pydantic import BaseModel

from app.models.job_application import ApplicationStatus


class JobApplicationCreate(BaseModel):
    company_id: int
    position: str
    description: str | None = None
    location: str | None = None
    salary: str | None = None
    application_date: datetime
    status: ApplicationStatus = ApplicationStatus.APPLIED
    notes: str | None = None


class JobApplicationResponse(BaseModel):
    id: int
    user_id: int
    company_id: int
    position: str
    description: str | None = None
    location: str | None = None
    salary: str | None = None
    application_date: datetime
    status: ApplicationStatus
    notes: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


class JobApplicationUpdate(BaseModel):
    company_id: int | None = None
    position: str | None = None
    description: str | None = None
    location: str | None = None
    salary: str | None = None
    application_date: datetime | None = None
    status: ApplicationStatus | None = None
    notes: str | None = None
