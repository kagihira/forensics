from fastapi import FastAPI, UploadFile, File, Form
import shutil
import os
import uuid
import json
from backend.extract_from_e01 import extract_files_from_e01
from backend.extract_text import extract_text_from_file
from backend.analyze_text import classify_text
from backend.compare_devices import compare_texts, compare_images, get_all_files

app = FastAPI()

UPLOAD_DIR = "uploads"
EXTRACTED_DIR = "data"

# 📂 Создаём папки, если их нет
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(EXTRACTED_DIR, exist_ok=True)

@app.post("/upload_e01/")
async def upload_e01(file: UploadFile = File(...), device_id: str = Form(...)):
    """
    Загружает `.E01`-файл и извлекает его файлы в папку устройства.
    """
    device_folder = os.path.join(EXTRACTED_DIR, device_id)
    os.makedirs(device_folder, exist_ok=True)

    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Извлекаем файлы в папку устройства
    extraction_success = extract_files_from_e01(file_path, device_folder)

    if not extraction_success:
        return {"error": "❌ Ошибка при извлечении файлов"}

    return {"message": f"✅ Файлы извлечены для {device_id} в {device_folder}"}

@app.get("/extract_text/{device_id}/")
async def extract_text_from_device(device_id: str):
    """
    Извлекает текст и хэши изображений из файлов устройства, включая вложенные папки.
    """
    device_folder = os.path.join(EXTRACTED_DIR, device_id)
    if not os.path.exists(device_folder):
        return {"error": f"❌ Устройство {device_id} не найдено"}

    extracted_data = {}

    for file_path in get_all_files(device_id):  # Теперь ищем во всех папках
        extracted_text = extract_text_from_file(file_path)
        extracted_data[file_path] = extracted_text

    # Сохраняем извлеченные данные в JSON
    extracted_text_file = os.path.join(device_folder, "extracted_text.json")
    with open(extracted_text_file, "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, indent=4)

    return {"message": f"✅ Текст и изображения извлечены для {device_id}", "data": extracted_data}

@app.get("/analyze_text/{device_id}/")
async def analyze_text_for_device(device_id: str):
    """
    Анализирует уже извлечённый текст из файлов устройства.
    """
    device_folder = os.path.join(EXTRACTED_DIR, device_id)
    extracted_text_file = os.path.join(device_folder, "extracted_text.json")

    if not os.path.exists(extracted_text_file):
        return {"error": f"❌ Нет извлечённого текста для {device_id}, сначала вызовите /extract_text/{device_id}/"}

    with open(extracted_text_file, "r", encoding="utf-8") as f:
        extracted_data = json.load(f)

    analyzed_results = {}
    for filename, text in extracted_data.items():
        classification = classify_text(text)
        analyzed_results[filename] = classification

    # Сохраняем анализ
    with open(f"{device_folder}/analysis_results.json", "w", encoding="utf-8") as f:
        json.dump(analyzed_results, f, indent=4)

    return {"message": f"✅ Текст проанализирован для {device_id}", "data": analyzed_results}

@app.get("/compare/")
async def compare_devices(device1: str, device2: str):
    """
    Сравнивает файлы между двумя устройствами.
    """
    matches = compare_texts(device1, device2)
    return {"matches": matches}

@app.get("/compare_images/")
async def compare_device_images(device1: str, device2: str):
    """
    Сравнивает изображения между двумя устройствами.
    """
    matches = compare_images(device1, device2)
    return {"image_matches": matches}
