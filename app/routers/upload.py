from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Form
from sqlalchemy.orm import Session
from typing import Optional
import shutil, os
from datetime import datetime
from app import crud, schemas, models, ai_module
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/upload", tags=["upload"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=schemas.ReefScanOut)
async def upload_coral_image(
    reef_name: str = Form(...),
    reef_location: str = Form(...),
    date_taken: Optional[datetime] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    reef = crud.get_reef_by_name(db, reef_name)
    if not reef:
        reef_in = schemas.ReefCreate(name=reef_name, location=reef_location)
        reef = crud.create_reef(db, reef_in)

    file_location = os.path.join(
        UPLOAD_DIR,
        f"{current_user.id}_{int(datetime.utcnow().timestamp())}_{file.filename}"
    )
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    diagnosis = ai_module.diagnose_coral(file_location)

    scan = crud.create_scan(
        db=db,
        user_id=current_user.id,
        reef_id=reef.id,
        image_path=file_location,
        date_taken=date_taken,
        diagnosis=diagnosis
    )
    return scan
