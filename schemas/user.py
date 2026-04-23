from pydantic import BaseModel, ConfigDict

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