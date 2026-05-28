from pydantic import BaseModel, Field
from datetime import datetime

# ==========================================
# BASE SCHEMAS (Data structures without relationships)
# ==========================================

class ItemBase(BaseModel):
    """
    Base schema for Item, containing core attributes.
    Used for reading or representing an Item entity.
    """
    id: int | None = None
    name: str  # This holds the unique text or URL extracted from the QR code
    description: str | None = None

    class Config:
        from_attributes = True


class ScanBase(BaseModel):
    """
    Base schema for a Scan event.
    Reflects the simplified database structure where Token is now an optional field.
    """
    id: int | None = None
    source: str  # Platform or source where the scan was triggered (e.g., 'Web')
    date: datetime | None = None
    token: str | None = None  # Optional field, can be Null if the QR has no token

    class Config:
        from_attributes = True


# ==========================================
# INPUT SCHEMAS (Data received from requests)
# ==========================================

class ScanCreate(BaseModel):
    """
    Schema required when a new scan occurs.
    Receives the raw QR text and metadata, then backend links it to an Item.
    """
    text: str = Field(..., min_length=1)   # Raw text/URL scanned from the QR code
    source: str = Field(..., min_length=1) # Origin of the scan event
    token: str | None = None  # Optional token string if present


# ==========================================
# RELATIONAL SCHEMAS (Nested structures for API responses)
# ==========================================

class ScanWithItem(ScanBase):
    """
    Response schema when retrieving a Scan, automatically embedding its linked Item.
    """
    item_id: int
    item: ItemBase

    class Config:
        from_attributes = True


class ItemWithScans(ItemBase):
    """
    Response schema when retrieving an Item, listing all its historical scan events.
    """
    scans: list[ScanBase] = []

    class Config:
        from_attributes = True


# ==========================================
# BACKWARD COMPATIBILITY ALIASES
# ==========================================

class Item(ItemBase):
    """Alias for basic Item operations to avoid breaking existing service references."""
    pass

class Scan(ScanBase):
    """Alias for basic Scan operations to avoid breaking existing service references."""
    pass
