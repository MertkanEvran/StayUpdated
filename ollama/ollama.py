# This script will check the ollama status and print it.
# It is designed to be run in a Python environment with the necessary packages installed.
import os
import requests
from typing import Optional, Dict
import producer
import consumer
import mongo

OLLAMA_URI = os.getenv("OLLAMA_URI", "http://localhost:11434")

def is_ollama_running() -> bool:
    try:
        response = requests.get(f"{OLLAMA_URI}")
        if response.text == "Ollama is running":
            return True
        return False
    except requests.RequestException:
        return False

def pull_model(model_name: str) -> bool:
    payload = {
        "model": model_name,
    }   
    try:
        response = requests.post(f"{OLLAMA_URI}/api/pull", json=payload)
        response.raise_for_status()
        print(f"{model_name} modeli başarıyla çekildi.")
        return True
    except requests.RequestException as e:
        print(f"{model_name} modeli çekilirken hata oluştu: {e}")
        return False
 
def is_model_loaded(model_name: str) -> bool:
    try:
        response = requests.get(f"{OLLAMA_URI}/api/tags")
        response.raise_for_status()
        response_data = response.json()
        response_models = [model['name'] for model in response_data.get('models', [])]
        if model_name in response_models:
            print(f"{model_name} modeli yüklü.")
            return True
        else:
            print(f"{model_name} modeli yüklü değil.")
            return False
    except requests.RequestException as e:
        print(f"{model_name} modeli kontrol edilirken hata oluştu: {e}")
        return False

def ask_to_model(prompt: str, model_name: str) -> str:
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(f"{OLLAMA_URI}/api/generate", json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "[Response not found]")
    except requests.RequestException as e:
        print(f"An error occurred while asking the model {model_name}: {e}")
        return "[Response not found]"

def build_prompt(article: Dict) -> str:

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

def main():
    _producer = producer.get_producer()  # Kafka producer'ı başlatılır
    _consumer = consumer.get_consumer()

    if not is_ollama_running():
        print("Ollama is not running. Exiting.")
        return
        
    if not is_model_loaded("gemma:latest"):
        if not pull_model("gemma:latest"):
            print("Failed to pull the gemma model. Exiting.")
            return
    
    for message in _consumer:
        try:
            article = message.value
            print(f"Yeni haber alındı: {article}")
            if "summary" not in article or "title" not in article:
                print("Gerekli alanlar yok, atlanıyor.")
                continue
            prompt = build_prompt(article)
            response = ask_to_model(prompt, "gemma:latest")
            producer.publish_message(_producer, {"title": article["title"], "summary": response})
            mongo.add_record_to_collection("news", "reports", {"title": article["title"], "report": response})

        except Exception as e:
            print(f"Hata oluştu: {e}")
            continue

    
if __name__ == "__main__":
    main()

