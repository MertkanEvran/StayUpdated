import logging
import os

# Log klasörü varsa kullan, yoksa oluştur
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Log dosyası adı (günlük)
log_file = os.path.join(log_dir, "app.log")

# Logger ayarı
logging.basicConfig(
    level=logging.INFO,  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()  # Terminale de yaz
    ]
)

# Logger'ı dışarı aktar
logger = logging.getLogger("mylogger")
