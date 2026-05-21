from pydantic import BaseModel
from datetime import datetime

class Item(BaseModel):
    name: str
    description: str | None = None

    class Config:
        from_attributes = True  # Pydantic v2 replacement for orm_mode

class Scan(BaseModel):
    text: str
    source: str
    date: datetime | None = None   # optional, backend sets it

    class Config:
        from_attributes = True

class Token(BaseModel):
    text: str
    source: str
    date: datetime | None = None   # optional, backend sets it
    item_id: int | None = None
    scan_id: int | None = None

    class Config:
        from_attributes = True
