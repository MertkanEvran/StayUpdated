import requests
from bs4 import BeautifulSoup
import sys
import os
import re
import json
from typing import List, Optional, Dict

# Bir üst klasörü yol listesine ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from logger import app_logger

URL = "https://www.artificialintelligence-news.com/artificial-intelligence-news/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_article_links() -> Optional[List[str]]:
    links = []
    try:
        response = requests.get(URL, headers=HEADERS)
        app_logger.info(f"Request sent to: {URL} | Headers: {HEADERS}")
        index_html = response.text
    except Exception as e:
        app_logger.error(f"Error sending request to: {URL} | Error: {e}")
        return None

    try:
        app_logger.info(f"Parsing HTML for {URL}")
        soup = BeautifulSoup(index_html, "html.parser")
        container = soup.find_all("div", class_="e-con-inner")[2]
        if container:
            loop_divs = container.find_all("div", attrs={"data-elementor-type": "loop-item"})
            for div in loop_divs:
                a_tag = div.find("a")
                if a_tag:
                    links.append(a_tag.get("href"))
            app_logger.info("Links fetched successfully.")
            return links
        else:
            app_logger.warning("Container element not found.")
            return None
    except Exception as e:
        app_logger.error(f"Error parsing HTML: {e}")
        return None

def get_article_json(link: str) -> Optional[Dict]:
    try:
        response = requests.get(link, headers=HEADERS)
        app_logger.info(f"Request sent to: {link} | Headers: {HEADERS}")
        index_html = response.text
    except Exception as e:
        app_logger.error(f"Error sending request to: {link} | Error: {e}")
        return None
    try:
        app_logger.info(f"Parsing HTML for {link}")
        soup = BeautifulSoup(index_html, "html.parser")
        # Title
        title_tag = soup.find("a", attrs={"href": link})
        title = title_tag.text if title_tag else "Başlık bulunamadı"
        app_logger.info(f"Title: {title}")
        # Author
        author_div = soup.find("div", class_=re.compile(r"^strip-after-comma-author-\\d+$"))
        author = author_div.find("a").text if author_div and author_div.find("a") else "Author not found"
        app_logger.info(f"Author: {author}")
        # Context
        context = ""
        content_div = soup.find("div", class_="elementor-widget-theme-post-content")
        if content_div:
            paragraphs = content_div.find_all("p")
            for p in paragraphs:
                context += p.get_text(strip=True) + "\n"
        else:
            app_logger.warning(f"Content not found: {link}")
        app_logger.info(f"Context (first 100 chars): {context[:100]}")
        article = {
            "author": author,
            "title": title,
            "context": context.strip()
        }
        return article
    except Exception as e:
        app_logger.error(f"Error fetching article data from {link}: {e}")
        return None

def append_article(article: Dict, filename: str = "articles.json") -> None:
    folder = "raw_data"
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    # Dosya var mı kontrolü
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    data = []
            except json.JSONDecodeError:
                data = []
    else:
        data = []
    # Aynı başlık varsa ekleme
    titles = {a.get("title") for a in data}
    if article.get("title") in titles:
        app_logger.info(f"Article with title '{article.get('title')}' already exists. Skipping.")
        return
    data.append(article)
    if not data:
        app_logger.info("No data to write. Skipping database write.")
        return
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    app_logger.info(f"Article added. Total articles: {len(data)}")

def update_articles() -> None:
    links = get_article_links()
    if not links:
        app_logger.warning("No links found. Update aborted.")
        return
    for link in links:
        article = get_article_json(link)
        if article:
            append_article(article)

