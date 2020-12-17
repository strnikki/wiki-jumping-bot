# wiki-jumping-bot
Bot that simulates the act of wiki jumping.

When used from the command line it only prints the name of the articles. 

```
usage: wiki_jumping_bot.py [-h] [-s STEPS] [-u URL]

simulate wiki jumping by printing all articles in a number of steps

optional arguments:
  -h, --help            show this help message and exit
  -s STEPS, --steps STEPS
                        number of articles to jump through
  -u URL, --url URL     url to the starting article
  ```

It is also possible to call the WikiJumpingBot class methods from another program.
The WikiJumpingBot public methods are:
 - return_titles_and_images: This method downloads the images for the first and last articles, if there are any. At the end it returns a dict, containing a list of titles named "titles", and a list named "images", with flags indicating if the first and last images were downloaded.
 - print_response: This method just print the contents of the "titles" list to stdout
