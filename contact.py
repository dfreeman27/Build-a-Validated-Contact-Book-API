from pydantic import BaseModel, Field, field_validator
from typing import Optional
from enum import Enum



class ContactCategory(str, Enum):

    personal = "personal"
    work = "work"
    family = "family"


class ContactCreate(BaseModel):
    """Schema for creating a new contact."""
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    category: ContactCategory = Field(...)

    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls, v):
        if "@" not in v:
            raise ValueError("email must contain @")
        return v


class ContactUpdate(BaseModel):
    """Schema for partially updating a contact (all fields optional)."""
  
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    category: Optional[ContactCategory] = Field(None)

    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls, v):
        if v is not None and "@" not in v:
            raise ValueError("email must contain @")
        return v


class ContactResponse(BaseModel):
    """Schema for returning contact data in API responses."""
    id: int
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    category: ContactCategory = Field(...)
    created_at: str 