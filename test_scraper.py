import scraper
import pytest
from requests.exceptions import HTTPError

def test_can_connect():
    assert (scraper.get_page_data("https://en.wikipedia.org/wiki/Web_scraping").status_code == 200)

def test_fail_to_connect():
    with pytest.raises(HTTPError):
        assert scraper.get_page_data("https://en.wikipedia.org/wiki/random_blabla")

def test_can_return_title():
    response = scraper.get_page_data("https://en.wikipedia.org/wiki/Web_scraping")
    soup = scraper.parse_html(response)

    assert (scraper.get_title(soup) == "Web scraping")

def test_can_return_link_to_new_article():
    links = ["https://en.wikipedia.org/wiki/Web_scraping", "https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol"]
    assert ("/wiki/" in scraper.get_new_article(links))

def test_does_not_follow_colon_links():
    links = ["https://en.wikipedia.org/wiki/Wikipedia:External_links"]
    with pytest.raises(Exception):
        assert scraper.get_new_article(links)

def test_does_not_follow_hashtag_links():
    links = ["https://en.wikipedia.org/wiki/Web_scraping#HTML_parsing"]
    with pytest.raises(Exception):
        assert scraper.get_new_article(links)

def test_get_new_article_fails_when_no_link():
    links = []
    with pytest.raises(Exception):
        assert scraper.get_new_article(links)

def test_can_return_list_of_titles():
    assert False