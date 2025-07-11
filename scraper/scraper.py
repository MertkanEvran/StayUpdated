from datetime import datetime
from utils import get_mongo_collection, parse_article_json, fetch_article_links, is_duplicate
import producer
import os


db_name = os.getenv("DB_NAME", "news")
collection_name = "articles"
topic = "raw-news"

def main():
    # MongoDB collection setup
    collection = get_mongo_collection(db_name, collection_name)

    _producer = producer.get_producer()  # Kafka producer'ı başlatılır
    
    # Fetch article links
    links = fetch_article_links()
    if not links:
        print("No links found or error fetching links.")
        return
    
    for link in links:
        article = parse_article_json(link)
        if article:
            if is_duplicate(article, db_name, collection_name):
                print(f"Duplicate article found: {article['title']}. Skipping...")
                continue

            
            print(f"Article fetched from {link}: {article['title']}")
            collection.insert_one(article.copy())
            print(f"Article from {link} saved successfully.")

            # Publish article to Kafka
            producer.publish_message(_producer, article, topic=topic)

            # Print article title and save to MongoDB
            print(f"Article published to Kafka: {article['title']}")

        else:
            print(f"Failed to parse article from {link}.")

if __name__ == "__main__":
    main()


