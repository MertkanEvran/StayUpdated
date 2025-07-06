import logging
import os

# Log klasörü varsa kullan, yoksa oluştur
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Log dosyası adı (günlük)
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Logger ayarı
logging.basicConfig(
    level=logging.INFO,  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()  # Terminale de yaz
    ]
)

# Logger'ı dışarı aktar
app_logger = logging.getLogger("stayupdated")
