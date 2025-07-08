import os
import smtplib
from email.message import EmailMessage
from pymongo import MongoClient
import json
from bson import ObjectId
from datetime import datetime

# Ortam değişkenlerinden bilgileri alalım
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
TO_EMAIL   = os.getenv("TO_EMAIL", SMTP_USER)  # İstersen kendine yollasın

def convert_for_json(obj):
    if isinstance(obj, list):
        return [convert_for_json(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: convert_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, datetime):
        return obj.isoformat()
    else:
        return obj

def load_report():
    client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
    db = client["news"]
    collection = db["reports"]
    report = collection.find_one(sort=[("created_at", -1)])  # En son eklenen raporu al
    if not report:
        return None
    return report.get("report", None)

def send_mail(content):
    if not content:
        print("❌ Rapor bulunamadı. Mail gönderilemiyor.")
        return
    
    msg = EmailMessage()
    msg["Subject"] = "Günlük LLM Raporun 📊"
    msg["From"] = SMTP_USER
    msg["To"] = TO_EMAIL


    msg.set_content(content)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.send_message(msg)
        print("✅ Mail gönderildi:", TO_EMAIL)

def main():
    content = load_report()
    send_mail(content)

if __name__ == "__main__":
    main()
