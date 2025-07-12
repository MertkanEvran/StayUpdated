import utils
import mongo
import producer
import os
import time


db_name = os.getenv("DB_NAME", "news")
collection_name = "articles"
topic = "raw-news"


def main():
    last_hash = None
    next_hash = None
    while True:
        content_div = utils.find_content_div()
        next_hash = utils.create_content_div_hash(content_div)
        if(not utils.is_hash_changed(last_hash, next_hash) and last_hash is not None):
            print("No changes detected in the content div. Waiting...")
            time.sleep(600)  # Wait before checking again
            continue
        _producer = producer.get_producer()  # Kafka producer'ı başlatılır
        
        # Fetch article links
        links = utils.fetch_article_links()
        if not links:
            print("No links found or error fetching links.")
            return
        
        for link in links:
            article = utils.fetch_article_data(link)
            if article:
                if utils.is_duplicate(article, db_name, collection_name):
                    print(f"Duplicate article found: {article['title']}. Skipping...")
                    continue

                
                print(f"Article fetched from {link}: {article['title']}")
                mongo.add_record_to_collection(db_name, collection_name, article.copy())

                # Publish article to Kafka
                producer.publish_message(_producer, article, topic=topic)

                # Print article title and save to MongoDB
                print(f"Article published to Kafka: {article['title']}")


            else:
                print(f"Failed to parse article from {link}.")

        last_hash = next_hash

if __name__ == "__main__":
    main()


