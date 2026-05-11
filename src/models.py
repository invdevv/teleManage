from pydantic import BaseModel

from datetime import datetime

class Account(BaseModel):
    id: int
    name: str
    
    created_at: float = datetime.now().timestamp()
    updated_at: float = datetime.now().timestamp()
