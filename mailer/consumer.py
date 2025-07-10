from kafka import KafkaConsumer
import json


default_parameters = {
    "topic": "raw-news",
    "group_id": 'my-group',
    "bootstrap_servers": 'kafka:9092',
    "auto_offset_reset": 'earliest',
    "enable_auto_commit": True,
    "value_deserializer": lambda x: json.loads(x.decode('utf-8'))
}

def init_consumer(params = default_parameters):
    """
    Kafka consumer fonksiyonu.
    Mesajları dinler ve alır.
    """
    
    consumer = KafkaConsumer(
        params["topic"],
        bootstrap_servers=params["bootstrap_servers"],
        auto_offset_reset=params["auto_offset_reset"],
        enable_auto_commit=params["enable_auto_commit"],
        group_id=params["group_id"],
        value_deserializer=params["value_deserializer"]
    )

    return consumer