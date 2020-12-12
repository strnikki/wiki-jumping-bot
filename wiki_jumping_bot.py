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

    bot = WikiJumpingBot()
    
    try:
        bot.print_response(n_steps=n_steps)
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

class WikiJumpingBot:

    def return_titles_and_images(self, n_steps=8, url="https://en.wikipedia.org/wiki/Special:Random"):
        data = self.__get_list_of_titles(url, n_steps)
        
        return data

    def print_response(self, n_steps=8, url="https://en.wikipedia.org/wiki/Special:Random"):
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
        # img = soup.find(id="content").find(class_="thumbimage")
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