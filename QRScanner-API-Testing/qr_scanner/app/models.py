from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Item(Base):
    """
    Represents the unique entity or product scanned.
    """
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    # The unique string or URL retrieved from the QR code
    name = Column(String, unique=True, index=True) 
    description = Column(String, index=True, nullable=True)

    # One-to-Many Relationship: One item can be scanned multiple times over time
    scans = relationship("Scan", back_populates="item", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Item id={self.id} name={self.name!r}>"


class Scan(Base):
    """
    Represents an individual physical scan event.
    Stores metadata about the scan event, including optional tokens.
    """
    __tablename__ = "scans"
    
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)  # Where the scan came from (e.g., 'Web', 'Mobile App')
    date = Column(DateTime, index=True)  # Timestamp of the scan event
    
    # Optional token extracted from the QR. It can be Null/None if the QR doesn't contain one
    token = Column(String, index=True, nullable=True) 

    # Foreign Key connecting this specific scan event directly to its Item
    item_id = Column(Integer, ForeignKey("items.id"))
    item = relationship("Item", back_populates="scans")

    def __repr__(self):
        return f"<Scan id={self.id} source={self.source!r} item_id={self.item_id} token={self.token!r}>"
