from PIL import Image
import imagehash
import os

def get_image_hash(image_path):
    """Генерирует pHash изображения"""
    try:
        image = Image.open(image_path).convert("L")  # Чёрно-белый режим
        return str(imagehash.phash(image))
    except Exception as e:
        print(f"⚠️ Ошибка при обработке {image_path}: {e}")
        return None  # Если не удалось обработать, возвращаем None

def extract_text_from_file(file_path):
    """Извлекает текст или pHash (если изображение)"""
    file_path = file_path.lower()  # Делаем имя файла в нижний регистр
    if file_path.endswith((".jpg", ".jpeg", ".png")):  # Теперь поддержка `.JPG`
        hash_value = get_image_hash(file_path)
        return hash_value if hash_value else "error"
    elif file_path.endswith(".txt"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"⚠️ Ошибка при чтении {file_path}: {e}")
            return "error"
    else:
        return "Unsupported file format"
