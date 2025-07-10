from datetime import datetime
from utils import get_mongo_collection, parse_article_json, fetch_article_links, is_duplicate
from producer import publish_message


db_name = "news"
collection_name = "articles"
topic = "raw-news"

def main():
    # MongoDB collection setup
    collection = get_mongo_collection(db_name, collection_name)
    
    # Fetch article links
    links = fetch_article_links()
    if not links:
        print("No links found or error fetching links.")
        return
    
    for link in links:
        article = parse_article_json(link)
        if article and not is_duplicate(article, db_name, collection_name):
            
            print(f"Article fetched from {link}: {article['title']}")
            collection.insert_one(article)
            print(f"Article from {link} saved successfully.")

            # Publish article to Kafka
            publish_message(article, topic=topic)

            # Print article title and save to MongoDB
            print(f"Article published to Kafka: {article['title']}")

        else:
            print(f"Failed to parse article from {link}.")

if __name__ == "__main__":
    main()


