import os
import json
from collections import defaultdict

EXTRACTED_DIR = "data"

def load_messages_data(device_id):
    """Загружает сообщения устройства"""
    messages_file = os.path.join(EXTRACTED_DIR, device_id, "messages.json")

    if not os.path.exists(messages_file):
        return {}

    with open(messages_file, "r", encoding="utf-8") as f:
        return json.load(f)

def analyze_conversations(device_id):
    """
    Анализирует переписку устройства и группирует сообщения по номерам телефонов.
    """
    messages = load_messages_data(device_id)
    if not messages:
        return {"error": f"❌ Нет сообщений для {device_id}"}

    conversations = defaultdict(list)

    for msg in messages:
        sender = msg.get("sender", "unknown")
        receiver = msg.get("receiver", "unknown")
        text = msg.get("text", "")

        conversations[f"{sender} ⇄ {receiver}"].append(text)

    return {"device_id": device_id, "conversations": conversations}

