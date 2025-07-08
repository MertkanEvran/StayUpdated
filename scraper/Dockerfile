# Python tabanlı hafif bir imaj
FROM python:3.11-slim

# Çalışma klasörü
WORKDIR /app

# Gerekli dosyaları kopyala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Uygulama başlatılacak komut
CMD ["python", "scraper.py"]