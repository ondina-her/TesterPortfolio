from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi import APIRouter, Request, Depends, HTTPException
from ..deps import get_db
from .. import crud, schemas, models

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")

@router.post("/items/", status_code=201, response_model=schemas.Item)
def create_item(item: schemas.Item, db: Session = Depends(get_db)):
    existing = db.query(models.Item).filter(models.Item.name == item.name).first()
    if existing:
        # Return existing item instead of error
        return existing

    return crud.create_item(db=db, item=item)
    Post
@router.get("/items/", status_code=200, response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_items(db=db, skip=skip, limit=limit)

@router.post("/scans/", status_code=201, response_model=schemas.Scan)
def create_scan(scan: schemas.Scan, db: Session = Depends(get_db)):
    existing = db.query(models.Scan).filter(models.Scan.text == scan.text).first()
    if existing:
        # Return existing scan instead of error
        return existing

    return crud.create_scan(db=db, scan=scan)

@router.get("/scans/", response_model=list[schemas.Scan])
def read_scans(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_scans(db=db, skip=skip, limit=limit)


@router.post("/tokens/", status_code=201, response_model=schemas.Token)
def create_token(token: schemas.Token, db: Session = Depends(get_db)):
    # Use token.item_id and token.scan_id directly
    if token.item_id and not db.query(models.Item).filter(models.Item.id == token.item_id).first():
        raise HTTPException(status_code=404, detail="Item not found")
    if token.scan_id and not db.query(models.Scan).filter(models.Scan.id == token.scan_id).first():
        raise HTTPException(status_code=404, detail="Scan not found")

    db_token = models.Token(
        text=token.text,
        source=token.source,
        date=token.date,
        item_id=token.item_id,
        scan_id=token.scan_id
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

@router.get("/tokens/", status_code=200, response_model=list[schemas.Token])
def read_tokens(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_tokens(db=db, skip=skip, limit=limit)
