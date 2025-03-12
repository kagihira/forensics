from fastapi import FastAPI, UploadFile, File
import shutil
import os
from backend.extract_from_e01 import extract_files_from_e01
from backend.extract_text import extract_text_from_file
from backend.analyze_text import classify_text

app = FastAPI()

UPLOAD_DIR = "uploads"
EXTRACTED_DIR = "data"

# 📂 Создаём папки, если их нет
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(EXTRACTED_DIR, exist_ok=True)

@app.post("/upload_e01/")
async def upload_e01(file: UploadFile = File(...)):
    """
    Загружает `E01`-файл и извлекает из него файлы.
    """
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # Сохраняем загруженный файл
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if not os.path.exists(file_path):
        return {"error": "❌ Файл не был загружен"}

    # Извлекаем файлы из E01
    extraction_success = extract_files_from_e01(file_path, EXTRACTED_DIR)

    if not extraction_success:
        return {"error": "❌ Ошибка при извлечении файлов из E01"}

    return {"message": f"✅ Файлы извлечены из {file.filename} в {EXTRACTED_DIR}"}

@app.get("/analyze_all/")
async def analyze_all():
    """
    Анализирует все файлы в папке /data
    """
    results = {}
    for filename in os.listdir(EXTRACTED_DIR):
        file_path = os.path.join(EXTRACTED_DIR, filename)
        text = extract_text_from_file(file_path)
        classification = classify_text(text)
        results[filename] = classification
    return results
