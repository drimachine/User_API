from pydantic import BaseModel, ConfigDict
from typing import Optional

class UserIn(BaseModel):
    name: str
    email: str
    role_id: int

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