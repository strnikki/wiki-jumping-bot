import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import random
import sys
import argparse

class OutOfLinksException(Exception): pass

def main():
    parser = argparse.ArgumentParser(description="simulate wiki jumping by printing all articles in a number of steps")
    parser.add_argument("-s", "--steps", type=int,
                        help="number of articles to jump through")
    parser.add_argument("-u", "--url", type=str,
                        help="url to the starting article")
    args = parser.parse_args()

    n_steps = args.steps or 8
    url = args.url or "https://en.wikipedia.org/wiki/Special:Random"

    bot = WikiJumpingBot()
    
    try:
        bot.print_response(n_steps=n_steps, url=url)
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

class WikiJumpingBot:

    def return_titles_and_images(self, n_steps=8, url="https://en.wikipedia.org/wiki/Special:Random"):
        """Return a dict and download images from the first
        and last article, if there are images available to download.

        The dict contains two keys: 
        - "title:   a list of each article's title
        - "images": a list of bools indicating if the corresponding
                    image was downloaded
           
        Keyword arguments:
        n_steps -- number of steps to jump from the starting article
        url     -- url to the starting article
        """
        data = self.__get_list_of_titles(url, n_steps)
        
        return data

    def print_response(self, n_steps=8, url="https://en.wikipedia.org/wiki/Special:Random"):
        """Print a list of each article's title

        Keyword arguments:
        n_steps -- number of steps to jump from the starting article
        url     -- url to the starting article
        """
        titles = self.__get_list_of_titles(url, n_steps)
        for title in titles["titles"]:
            print(title)

    def __get_page_data(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response

    def __get_title(self, soup):
        title = soup.find(id="firstHeading")
        return title.text

    def __get_new_article(self, soup):
        """Return a new article by selecting 
        a random link to an article in the 
        contents of the current article
        """
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


    def __get_article_image(self, soup, name):
        """Return the first image of the article.

        The method first search the infobox of the article 
        for an image.
        If that's not present, it search the contents of the 
        article for an image.
        """
        img = ""
        infobox = soup.find(id="content").find(class_="infobox")
        if infobox:
            img = infobox.img
        else:
           img = soup.find(id="content").find(class_="thumbimage")
        if img:
            url = "https:" + img["srcset"].split()[-2]

            r = requests.get(url)
            with open(name + ".jpg", "wb") as f:
                f.write(r.content)
            
            return True
        else:
            return False

    def __get_list_of_titles(self, url, n_steps):
        """Return a dict and download images from the first
        and last article, if there are images available to download.

        The dict contains two keys: 
        - "title:   a list of each article's title
        - "images": a list of bools indicating if the corresponding
                    image was downloaded
        """
        titles = []
        images = []
        data = {"titles" : titles, "images" : images}
        for i in range(n_steps):
            try:
                response = self.__get_page_data(url)
                soup = self.__parse_html(response.content)

                if i == 0:
                    result = self.__get_article_image(soup, "first")
                    data["images"].append(result)
                elif i == (n_steps - 1):
                    result = self.__get_article_image(soup, "last")
                    data["images"].append(result)

                title = self.__get_title(soup)
                data["titles"].append(title)
                url = self.__get_new_article(soup)
            except OutOfLinksException:
                break
        return data

    def __parse_html(self, response):
        soup = BeautifulSoup(response, 'html.parser')
        return soup

if __name__ == "__main__":
    main()