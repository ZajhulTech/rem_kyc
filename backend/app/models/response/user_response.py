from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4

class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
