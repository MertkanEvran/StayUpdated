from data_fetchers import ai_news
import config
from processors import chat_with_model

def main():

    ai_news.update_data()

if __name__ == "__main__":
    main()