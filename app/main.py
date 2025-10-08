import os
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Reef-Gen API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Paths ----------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------------- Mock Data ----------------
mock_users = [
    {"id": 1, "username": "diver_jane", "password": "123", "tokens": 50},
    {"id": 2, "username": "reef_keeper", "password": "abc", "tokens": 30},
]

mock_reefs = [
    {"id": 1, "name": "Great Barrier Reef", "location": "Australia"},
    {"id": 2, "name": "Belize Barrier Reef", "location": "Belize"},
    {"id": 3, "name": "Red Sea Coral Reef", "location": "Egypt"},
]

mock_scans = {
    1: [
        {
            "id": 1,
            "user_id": 1,
            "image_path": "/static/demo/reef1a.jpg",
            "date_taken": "2025-10-01T10:30:00",
            "diagnosis": "Healthy",
        }
    ]
}

# ---------------- Frontend Pages ----------------
@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/reef.html", response_class=HTMLResponse)
async def reef_page(request: Request):
    return templates.TemplateResponse("reef.html", {"request": request})

@app.get("/user.html", response_class=HTMLResponse)
async def user_page(request: Request):
    return templates.TemplateResponse("user.html", {"request": request})

@app.get("/login.html", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register.html", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# ---------------- Auth Endpoints ----------------
@app.post("/register")
async def register(username: str = Form(...), password: str = Form(...)):
    if any(u["username"] == username for u in mock_users):
        return {"error": "Username already exists"}
    new_id = len(mock_users) + 1
    new_user = {"id": new_id, "username": username, "password": password, "tokens": 10}
    mock_users.append(new_user)
    return {"message": "Registration successful", "user": new_user}

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    for u in mock_users:
        if u["username"] == username and u["password"] == password:
            return {"message": "Login successful", "user": u}
    return {"error": "Invalid credentials"}

# ---------------- API Endpoints ----------------
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    for u in mock_users:
        if u["id"] == user_id:
            return u
    return {"error": "User not found"}

@app.get("/users/{user_id}/scans")
async def get_user_scans(user_id: int):
    results = []
    for reef_id, scans in mock_scans.items():
        reef_name = next((r["name"] for r in mock_reefs if r["id"] == reef_id), "Unknown Reef")
        for s in scans:
            if s.get("user_id") == user_id:
                results.append({**s, "reef_id": reef_id, "reef_name": reef_name})
    return results

@app.get("/reefs")
async def list_reefs():
    reefs = []
    for r in mock_reefs:
        scans = mock_scans.get(r["id"], [])
        reefs.append({
            "id": r["id"],
            "name": r["name"],
            "location": r["location"],
            "scan_count": len(scans)
        })
    return reefs

@app.get("/reefs/{reef_id}")
async def get_reef(reef_id: int):
    for r in mock_reefs:
        if r["id"] == reef_id:
            return r
    return {"error": "Reef not found"}

@app.get("/reefs/{reef_id}/scans")
async def get_scans(reef_id: int):
    return mock_scans.get(reef_id, [])

@app.post("/reefs/{reef_id}/upload")
async def upload_scan(reef_id: int, user_id: int = Form(...), file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())

    new_scan = {
        "id": len(mock_scans.get(reef_id, [])) + 1,
        "user_id": user_id,
        "image_path": f"/static/uploads/{file.filename}",
        "date_taken": "2025-10-06T12:00:00",
        "diagnosis": "Pending AI",
    }

    if reef_id not in mock_scans:
        mock_scans[reef_id] = []
    mock_scans[reef_id].append(new_scan)

    for u in mock_users:
        if u["id"] == user_id:
            u["tokens"] += 5

    return {"message": "Scan uploaded successfully", "scan": new_scan, "tokens_awarded": 5}


