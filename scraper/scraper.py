from datetime import datetime
from utils import get_mongo_collection, fetch_html, parse_article_json, fetch_article_links

def main():
    # MongoDB collection setup
    collection = get_mongo_collection("news", "articles")
    
    # Fetch article links
    links = fetch_article_links()
    if not links:
        print("No links found or error fetching links.")
        return
    
    for link in links:
        article = parse_article_json(link)
        if article:
            print(f"Article fetched from {link}: {article['title']}")
            article['fetched_at'] = datetime.now().isoformat()
            article['url'] = link
            collection.insert_one(article)
            print(f"Article from {link} saved successfully.")
        else:
            print(f"Failed to parse article from {link}.")

if __name__ == "__main__":
    main()


