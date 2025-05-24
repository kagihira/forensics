from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Разрешаем доступ с фронтенда (порт 5500, 8001 или любой другой)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можно указать конкретный адрес фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
import shutil
import os
import uuid
import json
from backend.extract_from_e01 import extract_files_from_e01



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
EXTRACTED_DIR = "data"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(EXTRACTED_DIR, exist_ok=True)

@app.post("/upload_e01/")
async def upload_e01(file: UploadFile = File(...), device_id: str = Form(...)):
    e01_path = f"/tmp/{file.filename}"
    with open(e01_path, "wb") as f:
        f.write(await file.read())

    success = extract_files_from_e01(e01_path, device_id)
    if not success:
        return {"error": "❌ Не удалось извлечь файлы"}

    return {"message": f"✅ Готово! Файлы лежат в /data/{device_id}"}



