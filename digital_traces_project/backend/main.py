from fastapi import FastAPI, UploadFile, File
import shutil
from backend.extract_text import extract_text_from_pdf, extract_text_from_docx, extract_text_from_image
from backend.analyze_text import classify_text

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = f"data/{file.filename}"  # Сохраняем файл в папку data
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Определяем тип файла и извлекаем текст
    text = ""
    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file.filename.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    elif file.filename.endswith((".png", ".jpg", ".jpeg")):
        text = extract_text_from_image(file_path)
    else:
        return {"error": "Unsupported file format"}

    # Анализируем текст нейросетью
    classification = classify_text(text)

    return {
        "filename": file.filename,
        "extracted_text": text,  # Добавляем извлечённый текст
        "classification": classification  # Добавляем классификацию
    }
