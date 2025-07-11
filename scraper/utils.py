import requests
from bs4 import BeautifulSoup
import os
from pymongo import MongoClient
from typing import List, Optional, Dict
import re

URL = "https://www.artificialintelligence-news.com/artificial-intelligence-news/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_mongo_collection(db_name: str, collection_name: str):
    client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
    db = client[db_name]
    return db[collection_name]

def fetch_html(url: str, headers: Dict[str, str]) -> Optional[str]:
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    
def parse_article_json(link: str) -> Optional[Dict]:
    index_html = None
    try:
        response = requests.get(link, headers=HEADERS)
        index_html = response.text
        print(f"Fetched HTML for {link}")
    except Exception as e:
        print(f"Error fetching {link}: {e}")
        return None
    
    try:
        soup = BeautifulSoup(index_html, "html.parser")
        # Title
        title_tag = soup.find("a", attrs={"href": link})
        title = title_tag.text if title_tag else "Başlık bulunamadı"
        # Author
        author_div = soup.find("div", class_=re.compile(r"^strip-after-comma-author-\\d+$"))
        author = author_div.find("a").text if author_div and author_div.find("a") else "Author not found"
        # Context
        context = ""
        content_div = soup.find("div", class_="elementor-widget-theme-post-content")
        if content_div:
            print("Content div found, extracting paragraphs...")
            paragraphs = content_div.find_all("p")
            for p in paragraphs:
                context += p.get_text(strip=True) + "\n"

            # Data ID

        else:
            print("Content div not found, returning None.")
            return None
        
        article = {
            "link": link,
            "author": author,
            "title": title,
            "summary": context.strip(),
        }
        return article
    except Exception as e:
        print(f"Error parsing HTML for {link}: {e}")
        return None
    
def fetch_article_links() -> Optional[List[str]]:
    links = []
    fetch_html_content = fetch_html(URL, HEADERS)
    if not fetch_html_content:
        return None
    
    try:
        soup = BeautifulSoup(fetch_html_content, "html.parser")
        container = soup.find_all("div", class_="e-con-inner")[2]
        if container:
            loop_divs = container.find_all("div", attrs={"data-elementor-type": "loop-item"})
            for div in loop_divs:
                a_tag = div.find("a")
                if a_tag:
                    links.append(a_tag.get("href"))
            return links
        else:
            return None
    except Exception as e:
        return None
    
def is_duplicate(article: Dict, db_name: str, collection_name: str) -> bool:

    collection = get_mongo_collection(db_name, collection_name)
    existing_article = collection.find_one({"link": article["link"]})
    if existing_article:
        print(f"Duplicate found for article id: {article['link']}")
        return True
    return False

