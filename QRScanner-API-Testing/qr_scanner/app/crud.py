# crud.py - CRUD operations for the database
from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas
from fastapi import HTTPException

# ---- Item operations ----
def create_item(db: Session, item: schemas.Item):
    existing = db.query(models.Item).filter(models.Item.name == item.name).first()
    if existing:
        # Return the existing item instead of error
        return existing

    db_item = models.Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Item).offset(skip).limit(limit).all()

# ---- Scan operations ----
def create_scan(db: Session, scan: schemas.Scan):
    # Check if this scan already exists
    existing = db.query(models.Scan).filter(models.Scan.text == scan.text).first()
    if existing:
        # Return the existing scan instead of error
        return existing

    # Otherwise create a new one
    db_scan = models.Scan(
        text=scan.text,
        source=scan.source,
        date=datetime.utcnow(),
    )
    db.add(db_scan)
    db.commit()
    db.refresh(db_scan)
    return db_scan

def get_scans(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Scan).offset(skip).limit(limit).all()

# ---- Token operations ----
def create_token(db: Session, token: schemas.Token):
    # Optional: validate item_id and scan_id here if not already in router
    if token.item_id and not db.query(models.Item).filter(models.Item.id == token.item_id).first():
        raise HTTPException(status_code=404, detail="Item not found")
    if token.scan_id and not db.query(models.Scan).filter(models.Scan.id == token.scan_id).first():
        raise HTTPException(status_code=404, detail="Scan not found")

    db_token = models.Token(
        text=token.text,
        source=token.source,
        date=datetime.utcnow(),   # auto-set date instead of requiring client
        item_id=token.item_id,
        scan_id=token.scan_id,
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def get_tokens(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Token).offset(skip).limit(limit).all()
