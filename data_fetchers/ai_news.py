import requests
from bs4 import BeautifulSoup
import sys
import os

# Bir üst klasörü yol listesine ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from logger import logger

URL = "https://www.artificialintelligence-news.com/artificial-intelligence-news/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}



def get_links():
    links = []
    try:
        response = requests.get(URL, headers=headers)
        logger.info(f"Request sended to: {URL} /n Headers: {headers}")
        index_html = response.text
    except Exception as e:
        logger.error(f"An error occured while sending request to: {URL} /nError: {e}")
        return None

    # Get the all links for news
    try:
        logger.info(f"Starting to parsing proccess")
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
