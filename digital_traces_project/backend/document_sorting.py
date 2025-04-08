import os
import json

EXTRACTED_DIR = "data"


def load_analysis_results(device_id):
    """Загружает результаты анализа текста устройства"""
    analysis_file = os.path.join(EXTRACTED_DIR, device_id, "analysis_results.json")

    if not os.path.exists(analysis_file):
        return {}

    with open(analysis_file, "r", encoding="utf-8") as f:
        return json.load(f)


def sort_documents_by_risk(device_id):
    """
    Сортирует документы на "Опасные" и "Безопасные" на основе анализа.
    """
    analysis_results = load_analysis_results(device_id)
    if not analysis_results:
        return {"error": f"❌ Нет данных анализа для {device_id}"}

    dangerous_keywords = ["dangerous", "propaganda", "political", "religious", "legal"]

    sorted_documents = {"dangerous": [], "safe": []}

    for file, data in analysis_results.items():
        category = data.get("category", "neutral")
        if category in dangerous_keywords:
            sorted_documents["dangerous"].append(file)
        else:
            sorted_documents["safe"].append(file)

    return {"device_id": device_id, "sorted_documents": sorted_documents}
