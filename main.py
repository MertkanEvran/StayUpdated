from web_scraping import news_scrapper
from core import chat_with_model

def main():
    # Haberleri güncelle
    news_scrapper.update_articles()
    # Örnek: LLM ile sohbet (API anahtarı ve prompt örnek)
    # yanit = chat_with_model.ask_to_llm("Hello AI!", apikey="YOUR_API_KEY")
    # print(yanit)
    pass

if __name__ == "__main__":
    main()