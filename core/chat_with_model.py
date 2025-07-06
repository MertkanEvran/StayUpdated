import requests
import sys
import os
from typing import Optional

# Bir üst klasörü yol listesine ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from logger import app_logger

def ask_to_llm(prompt: str, apikey: str, model: str = "openrouter/cypher-alpha:free") -> Optional[str]:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {apikey}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://senin-site.com",  # isteğe bağlı
        "X-Title": "cypher-test"  # isteğe bağlı
    }
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    try:
        app_logger.info(f"Sending request to model: {model} with prompt: {prompt}")
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        answer = response_json["choices"][0]["message"]["content"]
        app_logger.info("Received response from model successfully.")
        return answer
    except requests.exceptions.HTTPError as http_err:
        app_logger.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        app_logger.error(f"Request exception: {req_err}")
    except KeyError:
        app_logger.error("Expected key not found in response JSON.")
    except Exception as e:
        app_logger.error(f"Unexpected error: {e}")
    return None
