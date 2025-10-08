# app/routers/mock.py
from fastapi import APIRouter

router = APIRouter()

# ---------------- MOCK DATA ----------------
mock_users = [
    {"id": 1, "username": "diver_jane", "tokens": 50},
    {"id": 2, "username": "reef_keeper", "tokens": 30},
]

mock_reefs = [
    {"id": 1, "name": "Bloody Bay Wall", "location": "Little Cayman"},
    {"id": 2, "name": "Trunk Bay Reef", "location": "St. John, USVI"},
]

mock_scans = {
    1: [
        {
            "id": 1,
            "image_path": "/static/demo/reef1a.jpg",
            "date_taken": "2025-10-01T10:30:00",
            "diagnosis": "Healthy",
        },
        {
            "id": 2,
            "image_path": "/static/demo/reef1b.jpg",
            "date_taken": "2025-10-03T14:10:00",
            "diagnosis": "Bleached",
        },
    ],
    2: [
        {
            "id": 3,
            "image_path": "/static/demo/reef2a.jpg",
            "date_taken": "2025-10-02T09:45:00",
            "diagnosis": "Diseased",
        }
    ],
}
# -------------------------------------------

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    for u in mock_users:
        if u["id"] == user_id:
            return u
    return {"error": "User not found"}

@router.get("/reefs")
async def list_reefs():
    return mock_reefs

@router.get("/reefs/{reef_id}")
async def get_reef(reef_id: int):
    for r in mock_reefs:
        if r["id"] == reef_id:
            return r
    return {"error": "Reef not found"}

@router.get("/reefs/{reef_id}/scans")
async def get_scans(reef_id: int):
    return mock_scans.get(reef_id, [])
