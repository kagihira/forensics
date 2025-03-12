from transformers import pipeline
import os
import json

# Загружаем предобученную NLP-модель (BERT/RoBERTa)
classifier = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-sentiment")

# Классификация текста по категориям
def classify_text(text):
    """
    Классифицирует текст по категориям: опасный, политика, религия, юриспруденция, пропаганда, сленг, обычный текст.
    """
    categories = {
        "dangerous": ["violence", "threat", "terrorism", "attack", "extremism"],
        "political": ["government", "election", "democracy", "law", "protest"],
        "religious": ["god", "church", "islam", "bible", "pray"],
        "legal": ["court", "lawyer", "contract", "judge", "law"],
        "propaganda": ["fake news", "manipulation", "disinformation"],
        "slang": ["dude", "bro", "wtf", "lol", "omg"],
        "neutral": []
    }

    # Анализ тональности (опасность)
    sentiment = classifier(text[:512])  # Ограничение до 512 символов
    sentiment_label = sentiment[0]['label']

    # Проверяем текст по категориям
    text_lower = text.lower()
    classified_category = "neutral"
    for category, keywords in categories.items():
        if any(keyword in text_lower for keyword in keywords):
            classified_category = category
            break

    return {
        "sentiment": sentiment_label,  # Опасный/нейтральный
        "category": classified_category  # Политика, религия и т. д.
    }

# Функция для обработки всех файлов в /data/
def analyze_all_files():
    """
    Загружает файлы из папки /data/, извлекает текст, анализирует и сохраняет результаты.
    """
    results = {}
    data_dir = "data"

    for filename in os.listdir(data_dir):
        file_path = os.path.join(data_dir, filename)

        if filename.endswith(".txt"):  # Можно расширить на PDF и другие форматы
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
                classification = classify_text(text)
                results[filename] = classification

    # Сохранение результатов в JSON
    with open("classification_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    return results
