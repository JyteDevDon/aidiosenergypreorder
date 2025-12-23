from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional

InstallType = Literal["Residential", "Commercial", "Industrial"]

class StatusOut(BaseModel):
    total_slots: int
    slots_remaining: int
    percent_remaining: int

class PriorityIn(BaseModel):
    full_name: str = Field(min_length=2, max_length=200)
    email: EmailStr
    whatsapp: str = Field(min_length=4, max_length=50)
    install_type: InstallType
    generator_size: str = Field(min_length=1, max_length=50, description="e.g., 75 kVA")
    daily_load: str = Field(min_length=1, max_length=50, description="e.g., 100 kW/h")

class PriorityOut(StatusOut):
    queue_id: str

class InsiderIn(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    whatsapp: str = Field(min_length=4, max_length=50)

class InsiderOut(BaseModel):
    ok: bool
