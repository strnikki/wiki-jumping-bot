import scraper
import pytest
from requests.exceptions import HTTPError

def test_can_connect():
    assert (scraper.get_page_data("https://en.wikipedia.org/wiki/Web_scraping").status_code == 200)

def test_fail_to_connect():
    with pytest.raises(HTTPError):
        assert scraper.get_page_data("https://en.wikipedia.org/wiki/random_blabla")

def test_can_return_title():
    assert (scraper.get_title() == "Title of Page")

def test_can_return_list_of_links():
    assert (type(scraper.get_links()) is list)

def test_can_return_list_of_titles():
    assert False