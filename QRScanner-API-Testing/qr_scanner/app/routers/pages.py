from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi import APIRouter, Request, Depends, HTTPException
from ..deps import get_db
from .. import crud, schemas, models
from pydantic import BaseModel

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# ==========================================
# CUSTOM RESPONSE SCHEMAS FOR WEB PAGES
# ==========================================

class ScanAndLinkResponse(BaseModel):
    """
    Optimized unified response model representing a single scan event
    and its main parent item. Token metadata now lives inside the scan field.
    """
    scan: schemas.Scan
    item: schemas.Item

    class Config:
        from_attributes = True


# ==========================================
# UNIFIED SCAN & LINK ENDPOINTS
# ==========================================

@router.get("/scan_and_link/", response_model=ScanAndLinkResponse)
def get_latest_scan(db: Session = Depends(get_db)):
    """
    Retrieves the most recent physical scan event recorded in the system,
    along with the data of the scanned unique Item.
    """
    # Fetch the latest scan sorted by ID
    latest_scan = db.query(models.Scan).order_by(models.Scan.id.desc()).first()
    if not latest_scan:
        raise HTTPException(status_code=404, detail="No scan logs found in database")
    
    # Retrieve the parent Item linked directly via Foreign Key
    item = db.query(models.Item).filter(models.Item.id == latest_scan.item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Parent item for this scan is missing")
    
    return ScanAndLinkResponse(
        scan=schemas.Scan.model_validate(latest_scan),
        item=schemas.Item.model_validate(item)
    )


@router.post("/scan_and_link/", response_model=ScanAndLinkResponse)
def scan_and_link(scan_data: schemas.ScanCreate, db: Session = Depends(get_db)):
    """
    Processes an incoming physical scan event.
    Creates or retrieves the unique Item based on raw text,
    then logs the Scan event linking it to that item with its optional token.
    """
    # 1. Process or fetch the Item entity (verifies unique name constraint automatically)
    db_item = crud.create_item(db=db, item=schemas.Item(name=scan_data.text, description=None))
    
    # 2. Log the physical Scan event directly linked to the Item ID
    db_scan = crud.create_scan(
        db=db, 
        source=scan_data.source, 
        item_id=db_item.id, 
        token=scan_data.token
    )

    return ScanAndLinkResponse(
        scan=schemas.Scan.model_validate(db_scan),
        item=schemas.Item.model_validate(db_item)
    )


@router.post("/scans/", status_code=201, response_model=ScanAndLinkResponse)
def create_scan(scan_data: schemas.ScanCreate, db: Session = Depends(get_db)):
    """
    Creates a scan event and links it to an Item.
    This is the RESTful alias for the scan-and-link workflow.
    """
    return scan_and_link(scan_data=scan_data, db=db)


# ==========================================
# GENERAL WEB VIEWS & READ ENDPOINTS
# ==========================================

@router.get("/")
async def index(request: Request):
    """Renders the primary web interface dashboard."""
    return templates.TemplateResponse(request, "index.html")


@router.get("/items/{item_id}", status_code=200, response_model=schemas.ItemWithScans)
def read_item(item_id: int, db: Session = Depends(get_db)):
    """Retrieves a specific unique Item record alongside its complete scan history."""
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item entity not found")
    return db_item


@router.get("/scans/{scan_id}", status_code=200, response_model=schemas.ScanWithItem)
def read_scan(scan_id: int, db: Session = Depends(get_db)):
    """Retrieves a single physical scan event data embedded with its linked parent Item."""
    db_scan = db.query(models.Scan).filter(models.Scan.id == scan_id).first()
    if not db_scan:
        raise HTTPException(status_code=404, detail="Scan record not found")
    return db_scan


@router.post("/items/", status_code=201, response_model=schemas.Item)
def create_item(item: schemas.Item, db: Session = Depends(get_db)):
    """Standalone endpoint to register new unique items manually into the database."""
    return crud.create_item(db=db, item=item)


@router.get("/items/", status_code=200, response_model=list[schemas.ItemWithScans])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieves a paginated list of items with their full historical scan lists."""
    return crud.get_items(db=db, skip=skip, limit=limit)


@router.get("/scans/", response_model=list[schemas.ScanWithItem])
def read_scans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieves a paginated timeline list of all individual physical scan events."""
    return crud.get_scans(db=db, skip=skip, limit=limit)
