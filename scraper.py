import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import random

def main():
    pass

def get_page_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response

def get_title(soup):
    title = soup.find(id="firstHeading")
    return title.text

def get_new_article(links):
    # allLinks = soup.body.find_all("a")
    # random.shuffle(allLinks)
    for link in links:
        if ("/wiki/" in link):
            link_split = link.split("/wiki/")
            if "#" in link_split[1] or ":" in link_split[1]:
                continue
            return link
    raise Exception("Out of links to follow")

def get_list_of_titles(url, n_steps):
    pass
    # titles = []
    # for i in range(n_steps):
    #     page_body = get_page_data(url).text
    #     titles.append(get_title(page_body))
    #     titles

def parse_html(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup