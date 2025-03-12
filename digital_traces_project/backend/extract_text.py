import pdfplumber
from docx import Document
import pytesseract
import cv2
import speech_recognition as sr
import sqlite3
import json
import os

# 📄 Извлекаем текст из PDF
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

# 📄 Извлекаем текст из DOCX
def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    return "\n".join([p.text for p in doc.paragraphs])

# 🖼 OCR (изображения → текст)
def extract_text_from_image(image_path):
    img = cv2.imread(image_path)
    text = pytesseract.image_to_string(img)
    return text

# 🎤 Распознавание речи из аудио
def extract_text_from_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    return text

# 💬 Чаты (WhatsApp, Telegram) из SQLite
def extract_text_from_chats(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT message FROM messages WHERE message IS NOT NULL")
    messages = "\n".join(row[0] for row in cursor.fetchall())
    conn.close()
    return messages

# 🛠 Главная функция обработки файла
def extract_text_from_file(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    elif file_path.endswith((".png", ".jpg")):
        return extract_text_from_image(file_path)
    elif file_path.endswith(".wav"):
        return extract_text_from_audio(file_path)
    elif file_path.endswith(".sqlite"):
        return extract_text_from_chats(file_path)
    else:
        return "Unsupported file format"
