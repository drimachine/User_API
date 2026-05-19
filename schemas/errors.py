from pydantic import BaseModel
from datetime import datetime, timezone

class ErrorDetail(BaseModel):
    status: int 
    error: str
    message: str
    path: str
    timestamp: str

    @classmethod
    def create(cls, status: int, error: str, message: str, path: str) -> ErrorDetail:
        return cls(
            status = status,
            error = error,
            message = message,
            path = path,
            timestamp = datetime.now(timezone.utc).isoformat(),
            
        )