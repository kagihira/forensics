import os
import json
from difflib import SequenceMatcher
from imagehash import hex_to_hash

EXTRACTED_DIR = "data"

def get_all_files(device_id):
    """Рекурсивно ищет все файлы в папке устройства"""
    device_folder = os.path.join(EXTRACTED_DIR, device_id)
    all_files = []

    for root, _, files in os.walk(device_folder):
        for filename in files:
            all_files.append(os.path.join(root, filename))

    return all_files

def load_text_data(device_id):
    """Загружает текстовые данные устройства"""
    analysis_file = os.path.join(EXTRACTED_DIR, device_id, "extracted_text.json")

    if not os.path.exists(analysis_file):
        return {}

    with open(analysis_file, "r", encoding="utf-8") as f:
        return json.load(f)

def compare_texts(device1, device2):
    """Сравнивает тексты между двумя устройствами"""
    data1 = load_text_data(device1)
    data2 = load_text_data(device2)

    similarities = []
    for file1, text1 in data1.items():
        for file2, text2 in data2.items():
            ratio = SequenceMatcher(None, text1, text2).ratio()
            if ratio > 0.8:  # 80% совпадения
                similarities.append((file1, file2, ratio))

    return similarities

def compare_images(device1, device2):
    """Сравнивает изображения по pHash"""
    data1 = load_text_data(device1)
    data2 = load_text_data(device2)

    print("🔍 Проверяем загруженные pHash:")
    print(f"📂 {device1}: {data1}")
    print(f"📂 {device2}: {data2}")

    image_matches = []
    for file1, hash1 in data1.items():
        if not file1.lower().endswith((".png", ".jpg", ".jpeg")):
            continue  

        for file2, hash2 in data2.items():
            if not file2.lower().endswith((".png", ".jpg", ".jpeg")):
                continue

            try:
                hash1_obj = hex_to_hash(hash1)
                hash2_obj = hex_to_hash(hash2)
                distance = hash1_obj - hash2_obj  

                print(f"🔍 Сравниваем {file1} и {file2} → Разница: {distance}")

                if distance < 20:  # УВЕЛИЧИЛИ ПОРОГ (раньше было 10)
                    image_matches.append((file1, file2, distance))

            except Exception as e:
                print(f"⚠️ Ошибка при сравнении {file1} и {file2}: {e}")

    return image_matches

