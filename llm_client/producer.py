from kafka import KafkaProducer
import json

# Producer objesi oluşturuyoruz
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',  # Docker network’ünde kafka servisi adıyla bağlanıyoruz
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Mesajı JSON'a çevirip byte’a dönüştürüyoruz
)


def publish_message(data, topic='raw-news'):
    """
    Kafka producer fonksiyonu.
    :param data: Gönderilecek veri (dict)
    :param topic: Hedef topic adı
    """
    try:
        producer.send(topic, value=data)
        producer.flush()
        print(f"Mesaj '{data}' topic '{topic}' üzerine gönderildi.")
    except Exception as e:
        print(f"Mesaj gönderilirken hata oluştu: {e}")

