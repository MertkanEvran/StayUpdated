import os
import requests
from pymongo import MongoClient
from typing import Optional, Dict
from datetime import datetime

OLLAMA_URI = os.getenv("OLLAMA_URI", "http://host.docker.internal:11434")
MONGO_URI = os.getenv("MONGO_URI")

def get_mongo_data() -> Optional[Dict]:
    if not MONGO_URI:
        print("MongoDB URI is not set.")
        return None
    
    try:
        client = MongoClient(MONGO_URI)
        db = client["news"]
        collection = db["articles"]
        articles = list(collection.find().sort("fetched_at", -1).limit(5))
        return articles
    
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None
    

def save_report_to_mongo(report_text: str):
    client = MongoClient(MONGO_URI)  # local MongoDB bağlantısı
    db = client["news"]
    collection = db["reports"]
    doc = {
        "report": report_text,
        "created_at": datetime.now()
    }
    result = collection.insert_one(doc)
    print(f"Rapor MongoDB'ye kaydedildi, id: {result.inserted_id}")


def build_prompt(articles):
    metin = "\n\n".join(
        f"Title: {a['title']}\Summary: {a['summary']}" for a in articles
    )
    return f"""Aşağıdaki haberleri oku ve bana türkçe kısa bir özet çıkar:

    {metin}

    Rapor net ve anlaşılır olsun. Madde madde olabilir."""

def call_ollama(prompt: str) -> str:
    payload = {
        "model": "gemma3",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(f"{OLLAMA_URI}/api/generate", json=payload)
    response.raise_for_status()
    data = response.json()
    return data.get("response", "[Yanıt bulunamadı]")

def main():
    articles = get_mongo_data()
    prompt = build_prompt(articles)
    report = call_ollama(prompt)

    # Dilersen burada dosyaya da yazabilirsin veya Mongo'ya ekleyebilirsin
    save_report_to_mongo(report)
    print("Rapor oluşturuldu ve MongoDB'ye kaydedildi.")

if __name__ == "__main__":
    main()