from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

    tokens = relationship("Token", back_populates="item", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Item id={self.id} name={self.name!r}>"


class Scan(Base):
    __tablename__ = "scans"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    source = Column(String, index=True)
    date = Column(DateTime, index=True)

    tokens = relationship("Token", back_populates="scan", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Scan id={self.id} text={self.text!r}>"


class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    source = Column(String, index=True)
    date = Column(DateTime, index=True)

    item_id = Column(Integer, ForeignKey("items.id"))
    item = relationship("Item", back_populates="tokens")

    scan_id = Column(Integer, ForeignKey("scans.id"))
    scan = relationship("Scan", back_populates="tokens")

    def __repr__(self):
        return f"<Token id={self.id} text={self.text!r} item_id={self.item_id} scan_id={self.scan_id}>"