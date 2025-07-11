import os
import smtplib
from email.message import EmailMessage
import consumer

# Ortam değişkenlerinden bilgileri alalım
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
TO_EMAIL   = os.getenv("TO_EMAIL", SMTP_USER)  # İstersen kendine yollasın


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
    _consumer = consumer.get_consumer()  # Kafka consumer'ı başlatılır
    for message in _consumer:
        report = message.value
        print(f"Yeni rapor alındı: {report}")
        send_mail(report)
        print("Rapor gönderildi.")
        

if __name__ == "__main__":
    main()
