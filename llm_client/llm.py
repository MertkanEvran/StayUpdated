import os
import requests
from pymongo import MongoClient
from typing import Optional, Dict
from datetime import datetime
import producer
import consumer

OLLAMA_URI = os.getenv("OLLAMA_URI", "http://host.docker.internal:11434")
MONGO_URI = os.getenv("MONGO_URI")

db_name = os.getenv("DB_NAME", "news")  # MongoDB veritabanı adı
collection_to_consume = "articles"
collection_to_publish = "reports"  # Raporların kaydedileceği koleksiyon
topic_to_consume = os.getenv("TOPIC_TO_CONSUME_LLM", "raw-news")  # Kafka'dan tüketeceğimiz topic
topic_to_publish = os.getenv("TOPIC_TO_PUBLISH_LLM", "reports")  # Kafka'ya göndereceğimiz topic

    
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
    if isinstance(articles, dict):
        articles = [articles]

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
    _producer = producer.get_producer()  # Kafka producer'ı başlatılır
    _consumer = consumer.get_consumer()

    for message in _consumer:
        article = message.value
        print(f"Yeni haber alındı: {article}")

        if "summary" not in article or "title" not in article:
            print("Gerekli alanlar yok, atlanıyor.")
            continue

        print("Haber özeti alındı, LLM için prompt hazırlanıyor...")
        prompt = build_prompt(article)

        print("Ollama ile rapor oluşturuluyor...")
        report = call_ollama(prompt)

        producer.publish_message(_producer, report, topic='reports')
        print("Rapor Kafka'ya gönderildi.")

        save_report_to_mongo(report)
        print("Rapor oluşturuldu ve MongoDB'ye kaydedildi.")

        

    print("Tüm haberler işlendi.")



if __name__ == "__main__":
    main()