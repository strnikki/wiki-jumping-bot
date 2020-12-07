import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup

def main():
    pass

def get_page_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response

def get_title(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find(id="firstHeading")
    return title.text

def get_links():
    pass

def get_list_of_titles(url, n_steps):
    pass
    # titles = []
    # for i in range(n_steps):
    #     page_body = get_page_data(url).text
    #     titles.append(get_title(page_body))
    #     titles
