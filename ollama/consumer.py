from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import time
import json
import os


llm_consumer_params = {
    "topic": os.getenv("TOPIC_TO_CONSUME_LLM", "raw-news"),
    "group_id": os.getenv("LLM_GROUP_ID", 'llm-client-group'),
    "bootstrap_servers": os.getenv("BOOTSTRAP_SERVER", 'kafka:9092'),
    "auto_offset_reset": 'earliest',
    "enable_auto_commit": True,
    "value_deserializer": lambda x: json.loads(x.decode('utf-8'))
}

_consumer = None  # Kafka consumer objesi global olarak tanımlanır

def get_consumer(topic=llm_consumer_params["topic"]) -> KafkaConsumer:
    """
    Kafka consumer objesini üretir (veya hazır varsa döner).
    Kafka hazır değilse belirli sayıda deneme yapar.
    """
    global _consumer
    if _consumer is not None:
        return _consumer

    for _ in range(10):
        try:
            _consumer = KafkaConsumer(
                topic,
                bootstrap_servers=llm_consumer_params["bootstrap_servers"],
                value_deserializer=llm_consumer_params["value_deserializer"],
                group_id= llm_consumer_params["group_id"],  # farklı consumer'lar aynı group içinde olursa mesajı paylaşırlar
                auto_offset_reset = llm_consumer_params["auto_offset_reset"],     # en son mesajlardan başla
                enable_auto_commit = llm_consumer_params["enable_auto_commit"]  # mesajları otomatik olarak commit et
            )
            print(f"Kafa consumer topic '{topic}' için hazır.")
            return _consumer
        except NoBrokersAvailable:
            print("Kafka broker'a ulaşılamadı. Tekrar deneniyor...")
            time.sleep(5)

    raise Exception("Kafka consumer oluşturulamadı.")