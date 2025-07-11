from kafka import KafkaProducer
import json
import os
from kafka.errors import NoBrokersAvailable
import time

_producer = None

def get_producer():
    global _producer
    if _producer is not None:
        return _producer
    
    for _ in range(10):
        try:
            _producer = KafkaProducer(
                bootstrap_servers=os.getenv("BOOTSTRAP_SERVER", "kafka:9092"),
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            return _producer
        except NoBrokersAvailable:
            print("Kafka hazır değil, bekleniyor...")
            time.sleep(5)

    raise Exception("Kafka producer oluşturulamadı.")


def publish_message(producer, data, topic=os.getenv("TOPIC_TO_PUBLISH_SCRAPER", "raw-news")):
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

