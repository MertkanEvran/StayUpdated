import os
import requests
from pymongo import MongoClient
from typing import Optional, Dict
from datetime import datetime
from producer import publish_message
from consumer import init_consumer

OLLAMA_URI = os.getenv("OLLAMA_URI", "http://host.docker.internal:11434")
MONGO_URI = os.getenv("MONGO_URI")

db_name = "news"
collection_to_consume = "articles"
collection_to_publish = "reports"
topic_to_consume = "raw-news"
topic_to_publish = "reports"

def get_mongo_data() -> Optional[Dict]:
    if not MONGO_URI:
        print("MongoDB URI is not set.")
        return None
    
    try:
        client = MongoClient(MONGO_URI)
        db = client[db_name]
        collection = db[collection_to_consume]
        articles = list(collection.find().sort("fetched_at", -1).limit(5))
        return articles
    
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None
    
def save_report_to_mongo(report_text: str):
    client = MongoClient(MONGO_URI)  # local MongoDB bağlantısı
    db = client[db_name]
    collection = db[collection_to_publish]
    doc = {
        "report": report_text,
        "created_at": datetime.now()
    }
    result = collection.insert_one(doc)
    print(f"Rapor MongoDB'ye kaydedildi, id: {result.inserted_id}")

def build_prompt(articles):
    metin = "\n\n".join(
        f"Başlık: {a['title']}\nÖzet: {a['summary']}" for a in articles
    )
    return f"""
    Aşağıdaki haberleri tamamen anla ve benim için Türkçe, akıcı, etkileyici ve sıkmayan bir özet çıkar.

    - Sadece en kritik ve bilmem gereken bilgileri ver.
    - Gereksiz detay ve tekrar olmasın.
    - Özetleri doğal bir anlatımla, sanki siteden okuyormuşum gibi yaz.
    - Özet madde madde olsun, her madde kısa ve net.
    - Her madde kendi içinde tamamlayıcı, kolay anlaşılır olsun.
    - Haberlerin ana fikrini ve önemli gelişmeleri vurgula.

    Haberler:
    {metin}

    Lütfen özeti, dikkatlice ve özenle hazırla."""

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

    for message in init_consumer():
        print(f"Yeni haber alındı: {message.value}")
        article_summary = message.value.get("summary", None)
        if article_summary is None:
            print("Haber özeti bulunamadı, atlanıyor.")
            continue

        print("Haber özeti alındı, LLM için prompt hazırlanıyor...")
        prompt = build_prompt(article_summary)
        
        print("Ollama ile rapor oluşturuluyor...")
        report = call_ollama(prompt)
        
        save_report_to_mongo(report)
        print("Rapor oluşturuldu ve MongoDB'ye kaydedildi.")

        publish_message(report, topic='reports')
        print("Rapor Kafka'ya gönderildi.")

    print("Tüm haberler işlendi.")

        
    

if __name__ == "__main__":
    main()