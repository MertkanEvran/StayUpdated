# StayUpdated - Otomatik Haber Takip ve Raporlama Sistemi

## Proje Hakkında

StayUpdated, internetten haberleri otomatik olarak çeken, veritabanında (MongoDB) saklayan, güçlü bir LLM (Ollama ile Gemma3 modeli) kullanarak bu haberlerden anlamlı ve özlü raporlar hazırlayan ve raporları e-posta yoluyla gönderen bir proje.

Bu sayede güncel gelişmeleri sürekli takip etmek, önemli haberleri kaçırmamak mümkün oluyor. Sistem modüler yapısıyla haber çekme, LLM analizi ve mail gönderimi adımlarını birbirinden bağımsız çalıştırabiliyor.

---

## Nasıl Geliştirildi?

- **Scraper**: Web scraping yaparak haber başlıkları ve özetleri çekiyor.
- **MongoDB**: Haber verileri MongoDB'de depolanıyor.
- **LLM Client**: Ollama platformunda çalışan Gemma3 modeli ile haberlerden anlamlı özetler oluşturuluyor.
- **Mailer**: Oluşturulan raporları belirlenen e-posta adresine gönderiyor.
- **Docker & Docker Compose**: Tüm servisler docker container'ları içinde çalışıyor; böylece kurulumu ve yönetimi kolaylaşıyor.
- **Pipeline**: Python scripti ile bu adımlar sırasıyla çalıştırılarak otomatik bir süreç sağlanıyor.

---

## Kurulum ve Çalıştırma

### Ön Koşullar

- Docker ve Docker Compose sisteminizde kurulu olmalı.
- Ollama uygulaması bilgisayarınızda yüklü ve kullanılabilir durumda olmalı.
- `.env` dosyası oluşturulmalı ve aşağıdaki ortam değişkenleri tanımlanmalı:

```env
MONGO_URI=mongodb://localhost:27017/
OLLAMA_ENDPOINT=http://localhost:11434
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=senin.email@gmail.com
SMTP_PASS=mailşifren
TO_EMAIL=alici.email@gmail.com

### Çalıştırma
    - Tek yapmanız gereken main.py dosyasını çalıştırmak. Birkaç dakika içerisinde raporunuz mailinize gönderilicektir.