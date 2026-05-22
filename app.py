from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from modules.ocr import extract_text
from modules.rules import detect_violations
from modules.rights import get_rights_response

app = FastAPI()

# ✅ CORS (FIXED - IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # safe for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"status": "backend running 🚀"}


# ---------------- SCAN CHALLAN ----------------
@app.post("/scan-challan")
async def scan_challan(file: UploadFile = File(...)):

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text(file_path)
    violations = detect_violations(text)

    total_fine = sum(v["fine"] for v in violations) if violations else 0

    return {
        "ocr_text": text,
        "violations": violations,
        "total_fine": total_fine,
        "status": "success"
    }


# ---------------- RIGHTS API ----------------
@app.get("/know-rights")
def know_rights():
    return get_rights_response()