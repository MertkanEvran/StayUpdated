import requests
from bs4 import BeautifulSoup

URL = "https://www.artificialintelligence-news.com/artificial-intelligence-news/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

links = []

# Get the html of main web page

response = requests.get(URL, headers=headers)
index_html = response.text

# Get the all links for news

soup = BeautifulSoup(index_html, "html.parser")


container = soup.find_all("div", class_="e-con-inner")[2]
if container:
    loop_divs = container.find_all("div", attrs={"data-elementor-type": "loop-item"})
    for div in loop_divs:
        a_tag = div.find("a")
        if a_tag:
            links.append(a_tag.get("href"))
else:
    print("elementor-loop-container bulunamadı.")
