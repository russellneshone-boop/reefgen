from fastapi import APIRouter

router = APIRouter(prefix="/diagnosis", tags=["diagnosis"])

@router.get("/")
def read_status():
    return {"status": "Diagnosis endpoint placeholder"}
