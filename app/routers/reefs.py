from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.database import get_db

router = APIRouter(prefix="/reefs", tags=["reefs"])

@router.get("/{reef_id}/scans", response_model=List[schemas.ReefScanOut])
def get_scans_for_reef(reef_id: int, db: Session = Depends(get_db)):
    scans = crud.get_scans_by_reef(db, reef_id)
    if not scans:
        raise HTTPException(status_code=404, detail="No scans found for this reef")
    return scans
