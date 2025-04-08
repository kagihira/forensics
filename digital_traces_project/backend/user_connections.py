import os
import json
from collections import defaultdict

EXTRACTED_DIR = "data"

def load_messages_data(device_id):
    """Загружает переписку пользователя"""
    messages_file = os.path.join(EXTRACTED_DIR, device_id, "messages.json")

    if not os.path.exists(messages_file):
        return []

    with open(messages_file, "r", encoding="utf-8") as f:
        return json.load(f)

def load_contacts_data(device_id):
    """Загружает список контактов пользователя"""
    contacts_file = os.path.join(EXTRACTED_DIR, device_id, "contacts.json")

    if not os.path.exists(contacts_file):
        return []

    with open(contacts_file, "r", encoding="utf-8") as f:
        return json.load(f)

def find_user_connections(device_id):
    """
    Анализирует переписку и контакты пользователя, чтобы найти связи с другими пользователями.
    """
    messages = load_messages_data(device_id)
    contacts = load_contacts_data(device_id)

    connections = defaultdict(set)

    for msg in messages:
        sender = msg.get("sender", "unknown")
        receiver = msg.get("receiver", "unknown")

        connections[sender].add(receiver)
        connections[receiver].add(sender)

    for contact in contacts:
        user = contact.get("owner", "unknown")
        contact_number = contact.get("contact_number", "unknown")

        connections[user].add(contact_number)
        connections[contact_number].add(user)

    connections = {user: list(conns) for user, conns in connections.items()}

    return {"device_id": device_id, "connections": connections}
