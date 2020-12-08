import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import random

class OutOfLinksException(Exception): pass

def main():
    pass

def get_page_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response

def get_title(soup):
    title = soup.find(id="firstHeading")
    return title.text

def get_new_article(soup):
    allLinks = soup.find(id="content").find_all("a")
    random.shuffle(allLinks)

    for link in allLinks:
        link = link.get("href", "")
        if "/wiki/" in link:
            if "#" in link or ":" in link:
                continue
            link = "https://en.wikipedia.org" + link
            return link
    raise OutOfLinksException("Out of links to follow")

def get_list_of_titles(url, n_steps):
    titles = []
    for _ in range(n_steps):
        response = get_page_data(url)
        soup = parse_html(response.content)
        title = get_title(soup)
        titles.append(title)
        url = get_new_article(soup)
    return titles

def parse_html(response):
    soup = BeautifulSoup(response, 'html.parser')
    return soup
