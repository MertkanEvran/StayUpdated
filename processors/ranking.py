import requests

import sys
import os

# Bir üst klasörü yol listesine ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import config

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": "Bearer {}".format(config.APIKEY),
    "Content-Type": "application/json",
    "HTTP-Referer": "https://senin-site.com",  # zorunlu değil ama tavsiye edilir
    "X-Title": "cypher-test"  # isteğe bağlı
}

data = {
    "model": "openrouter/cypher-alpha:free",
    "messages": [
        {"role": "user", "content": "A farmer has 17 sheep. All but 9 run away. How many are left?"}
    ]
}

response = requests.post(url, headers=headers, json=data)
# 1. Önce JSON olarak parse et
response_json = response.json()

# 2. Sonra içinden cevabı çek
print(response_json["choices"][0]["message"]["content"])
