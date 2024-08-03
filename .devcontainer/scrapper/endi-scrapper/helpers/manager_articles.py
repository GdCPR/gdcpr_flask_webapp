import bs4
import requests
import hashlib
import dateparser
from bs4 import BeautifulSoup
from helpers import constants_articles

def current_articles(url = constants_articles.URL) -> bs4.ResultSet:
    """
    Extract current articles from url.

    :param url: A url of news articles section to be scrapped
    :type url: str, optional
    :return: A subclass from python list that keeps track of the SoupStrainer
    :rtype: bs4.ResultSet 
    """
    # Get request to base url
    sess = requests.Session()
    response = sess.get(url=url)

    # Creating HTML soup text content with bs4 HTML parser
    soup = BeautifulSoup(response.text,
                             'html.parser')

    # Find all articles by tag and class specification
    articles = soup.find_all(**constants_articles.articles_element)

    return articles

class Article:
    """
    This is an object that models a conceptual article structure

    :param article: Parse tree HTML tag with its attributes and contents
    :type article: bs4.elemet.Tag
    """
    def __init__(self, article: bs4.element.Tag) -> None:
        """
        Model constructor

        :param article: Parse tree HTML tag with its attributes and contents
        :type article: bs4.elemet.Tag
        """
        self.article = article

    def get_hash(self) -> dict:
        """
        Maps article tag objecto to fixed-size value

        :return: A dictionary containing hash value
        :rtype: dict
        """
        # Create hash object
        hash_object = hashlib.sha256(self.article.encode('utf-8'))
        # Get the hexadecimal representation of hash object
        self.hash_hex_digest = hash_object.hexdigest()

        return {"hash": self.hash_hex_digest}
    def _url(self):
        """Extract article path"""
        article_path = self.article.find(**constants_articles.url_element)
        article_path = article_path["href"]# type: ignore
        # Create article full url
        self.article_url = f"{constants_articles.BASE_URL}{article_path}"

    def _headline(self):
        """Extract article headline"""
        # Create an iterator to separate headline from subheadline
        headlines = self.article.find(**constants_articles.headline_element)
        headlines_iterator = headlines.stripped_strings # type: ignore
        # Fetch the first item only which corresponds to the headline
        self.article_hl = next(headlines_iterator)
    
    def _author(self):    
        """Extract article author"""
        html_attrs_dict = {"class": "authors-byline-text"}
        author = self.article.find(**constants_articles.author_element)
        author = author.text.strip() # type: ignore
        self.author = author[4:] # remove "Por " portion from the string

    def _article_soup(self):
        pass

    def _subheadline(self):
        pass