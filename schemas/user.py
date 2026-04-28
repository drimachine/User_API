from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional

class UserIn(BaseModel):
    name: str
    email: str
    role_id: int

    @field_validator('email')
    @classmethod
    def email_validation(cls, value: str):
        email = value.lower()
        return email

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    role_id: int

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role_id: Optional[int] = None