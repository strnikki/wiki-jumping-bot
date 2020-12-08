import scraper
from scraper import OutOfLinksException
import pytest
from requests.exceptions import HTTPError

def test_can_connect():
    assert (scraper.get_page_data("https://en.wikipedia.org/wiki/Web_scraping").status_code == 200)

def test_fail_to_connect():
    with pytest.raises(HTTPError):
        assert scraper.get_page_data("https://en.wikipedia.org/wiki/random_blabla")

def test_can_return_title():
    response = scraper.get_page_data("https://en.wikipedia.org/wiki/Web_scraping")
    soup = scraper.parse_html(response.content)

    assert (scraper.get_title(soup) == "Web scraping")

def test_can_return_link_to_new_article():
    
    response = '<div id="content"><a href="/wiki/Web_scraping"></a></div>'
    soup = scraper.parse_html(response)

    link = scraper.get_new_article(soup)
    assert link == "https://en.wikipedia.org/wiki/Web_scraping"

def test_does_not_follow_colon_links():
    response = '<div id="content"><a href="/wiki/Web_scraping:Something"></a></div>'
    soup = scraper.parse_html(response)

    with pytest.raises(OutOfLinksException):
        assert scraper.get_new_article(soup)

def test_does_not_follow_hashtag_links():
    response = '<div id="content"><a href="/wiki/Web_scraping#Something"></a></div>'
    soup = scraper.parse_html(response)

    with pytest.raises(OutOfLinksException):
        assert scraper.get_new_article(soup)

def test_get_new_article_fails_when_no_link():
    response = '<div id="content"></div>'
    soup = scraper.parse_html(response)

    with pytest.raises(OutOfLinksException):
        assert scraper.get_new_article(soup)

def test_can_get_links_from_soup():
    pass
    

def test_can_return_list_of_titles():
    # titles = scraper.get_list_of_titles("https://en.wikipedia.org/wiki/Web_scraping", 5)
    # assert len(titles) == 5
    assert False