from pydantic import BaseModel, ConfigDict

class RoleIn(BaseModel):
    name: str

class RoleOut(BaseModel): 
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str