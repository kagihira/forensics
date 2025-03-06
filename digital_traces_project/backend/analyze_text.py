from transformers import pipeline

# Загружаем предобученную модель BERT
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# Функция для анализа текста
def classify_text(text):
    result = classifier(text)
    return result
