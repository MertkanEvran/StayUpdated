import requests
from bs4 import BeautifulSoup
import sys
import os
import re
import json

# Bir üst klasörü yol listesine ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from logger import logger

URL = "https://www.artificialintelligence-news.com/artificial-intelligence-news/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}



def get_links():
    links = []
    index_html = None
    try:
        response = requests.get(URL, headers=headers)
        logger.info(f"Request sended to: {URL} /n Headers: {headers}")
        index_html = response.text
    except Exception as e:
        logger.error(f"An error occured while sending request to: {URL} /nError: {e}")
        return None

    # Get the all links for news
    try:
        logger.info(f"Starting to parsing proccess for {URL}")
        soup = BeautifulSoup(index_html, "html.parser")

        container = soup.find_all("div", class_="e-con-inner")[2]
        if container:
            loop_divs = container.find_all("div", attrs={"data-elementor-type": "loop-item"})
            for div in loop_divs:
                a_tag = div.find("a")
                if a_tag:
                    links.append(a_tag.get("href"))

            logger.info("The links returned succesfuly.")
            return links
        else:
            logger.info(f"The container element does not found.")
            return None
    except Exception as e:
        logger.error(f"An error occured while parsing the html/nError: {e}")
        return None

def get_link_context(link):


    index_html = None

    try:
        response = requests.get(link, headers=headers)
        logger.info(f"Request sended to: {link} /n Headers: {headers}")
        index_html = response.text
    except Exception as e:
        logger.error(f"An error occured while sending request to: {link} /nError: {e}")
        return None
    
    try:
        logger.info(f"Starting to parsing proccess for {link}")
        soup = BeautifulSoup(index_html, "html.parser")

        logger.info(f"Html parsed for {link}")
        logger.info(f"Starting to fetching data in  {link}")

        # Title
        title_tag = soup.find("a", attrs={"href": link})
        title = title_tag.text if title_tag else "Başlık bulunamadı"
        logger.info(f"Title fetched as {title}")

        # Author
        author_div = soup.find("div", class_=re.compile(r"^strip-after-comma-author-\d+$"))
        author = author_div.find("a").text if author_div and author_div.find("a") else "Author does not found"
        logger.info(f"Author fetched as {author}")

        # Context (yazı içeriği)
        context = ""
        content_div = soup.find("div", class_="elementor-widget-theme-post-content")
        if content_div:
            paragraphs = content_div.find_all("p")
            for p in paragraphs:
                context += p.get_text(strip=True) + "\n"
        else:
            logger.warning(f"Content does not found: {link}")

        logger.info(f"Context fetched (First 100 letter): {context[:100]}")

        article = {
            "author": author,
            "title": title,
            "context": context.strip()
        }

        return article

    except Exception as e:
        logger.error(f"An error occured while fetching data about article from {link}. Hata: {e}")
        return None
    
def append_article(article, filename="articles.json"):
    folder = "raw_data"
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)

    # Önce dosya var mı diye kontrol et, varsa oku
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

    # Yeni article'ı ekle
    
    data.append(article)

    if not data:
        logger.info("The data is empty. Returning from writing data to database")
        return

    # Tekrar dosyaya yaz
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    logger.info((f"Article added. Total articles: {len(data)}"))