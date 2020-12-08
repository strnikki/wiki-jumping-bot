import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import random
import sys

class OutOfLinksException(Exception): pass

def main():
    if len(sys.argv) > 1:
        n_steps = int(sys.argv[1])
    else:
        n_steps = 8
    
    try:
        titles = get_list_of_titles("https://en.wikipedia.org/wiki/Special:Random", n_steps)
        for title in titles:
            print(title)
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")


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

if __name__ == "__main__":
    main()