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
from backend.extract_text import extract_text_from_file
from backend.analyze_text import classify_text
from backend.compare_devices import compare_texts, compare_images, get_all_files
from backend.messages_analysis import analyze_conversations
from backend.document_sorting import sort_documents_by_risk
from backend.user_connections import find_user_connections


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



@app.get("/extract_text/{device_id}/")
async def extract_text_from_device(device_id: str):
    """
    Извлекает текст и хэши изображений из файлов устройства, включая вложенные папки.
    """
    device_folder = os.path.join(EXTRACTED_DIR, device_id)
    if not os.path.exists(device_folder):
        return {"error": f"❌ Устройство {device_id} не найдено"}

    extracted_data = {}

    for file_path in get_all_files(device_id):
        extracted_text = extract_text_from_file(file_path)
        extracted_data[file_path] = extracted_text

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


@app.get("/analyze_messages/{device_id}/")
async def analyze_messages(device_id: str):
    """
    Анализирует переписку между номерами телефона на устройстве.
    """
    result = analyze_conversations(device_id)
    return result

@app.get("/sort_documents/{device_id}/")
async def sort_documents(device_id: str):
    """
    Сортирует документы на "Опасные" и "Безопасные".
    """
    result = sort_documents_by_risk(device_id)
    return result

@app.get("/find_connections/{device_id}/")
async def find_connections(device_id: str):
    """
    Поиск связей между пользователями на основе переписки и контактов.
    """
    result = find_user_connections(device_id)
    return result


@app.get("/analyze_messages/{device_id}/")
async def analyze_messages(device_id: str):
    """
    Анализирует переписку между номерами телефона на устройстве.
    """
    result = analyze_conversations(device_id)
    return result

@app.get("/sort_documents/{device_id}/")
async def sort_documents(device_id: str):
    """
    Сортирует документы на "Опасные" и "Безопасные".
    """
    result = sort_documents_by_risk(device_id)
    return result

@app.get("/find_connections/{device_id}/")
async def find_connections(device_id: str):
    """
    Поиск связей между пользователями на основе переписки и контактов.
    """
    result = find_user_connections(device_id)
    return result