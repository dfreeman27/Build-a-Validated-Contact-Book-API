
from fastapi import APIRouter, HTTPException, status
from app.schemas import contact
from app.schemas.contact import ContactCreate, ContactUpdate, ContactResponse, ContactCategory

from typing import Optional
from datetime import datetime

router = APIRouter()

# In-memory storage
contacts: list[dict] = []
_next_id = 1


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(contact: ContactCreate):
    """
    Creates a new contact.
    """
    
    global _next_id
    new_contact = contact.model_dump()
    new_contact["id"] = _next_id
    new_contact["created_at"] = datetime.utcnow().isoformat()
    contacts.append(new_contact)
    _next_id += 1
    return new_contact


@router.get("/", response_model=list[ContactResponse])
def list_contacts(category: Optional[ContactCategory] = None):
    """
    Returns all contacts.
    """
    if category:
        filtered_contacts = [c for c in contacts if c["category"] == category]
        return filtered_contacts
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int):
    """
    Returns a single contact by ID.
    """

    for contact in contacts:
        if contact["id"] == contact_id:
            return contact
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")


@router.patch("/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact_data: ContactUpdate):
    """
    Partially updates a contact.
    """
    
    for contact in contacts:
        if contact["id"] == contact_id:
            update_data = contact_data.model_dump(exclude_unset=True)
            contact.update(update_data)
            return contact
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")