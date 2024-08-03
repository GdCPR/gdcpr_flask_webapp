"""
Module that acts as an article manager
"""
import requests
import hashlib
import dateparser
from bs4 import BeautifulSoup, ResultSet, element
from helpers import constants_articles


def current_articles(url = constants_articles.URL) -> ResultSet:
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
    def __init__(self, tag: element.Tag) -> None:
        """
        Model constructor

        :param article_tag: Parse tree HTML tag with its attributes and contents
        :type article: bs4.elemet.Tag
        """
        self.article = tag
        self.article_soup = None

    def get_hash(self) -> dict:
        """
        Maps article tag objecto to fixed-size value

        :return: A dictionary containing hash value
        :rtype: dict
        """
        # Create hash object
        hash_object = hashlib.sha256(self.article.encode('utf-8'))
        # Get the hexadecimal representation of hash object
        self.hash = hash_object.hexdigest()
        return {"hash": self.hash}
    
    def _url(self):
        """Extract article url"""
        article_path = self.article.find(**constants_articles.url_element)
        article_path = article_path["href"]# type: ignore
        # Create article full url
        self.url = f"{constants_articles.BASE_URL}{article_path}"

    def _headline(self):
        """Extract article headline"""
        # Create an iterator to separate headline from subheadline
        hls = self.article.find(**constants_articles.headline_element)
        hls_iterator = hls.stripped_strings # type: ignore
        # Fetch the first item only which corresponds to the headline
        self.headline = next(hls_iterator)
    
    def _author(self):    
        """Extract article author"""
        author = self.article.find(**constants_articles.author_element)
        author = author.text.strip() # type: ignore
        self.author = author[4:] # remove "Por " portion from the string

    def _subheadline(self):
        """Extract article subheadline"""
        if self.article_soup is None:
            sess = requests.session()
            self._url()
            response = sess.get(self.url)
            self.article_soup = BeautifulSoup(response.text,
                                         "html.parser")
            shl = self.article_soup.find(**constants_articles.subheadline_element)
            shl = shl.text # type: ignore
            shl = shl.strip()
            self.subheadline = shl
        else:
            shl = self.article_soup.find(**constants_articles.subheadline_element)
            shl = shl.text # type: ignore
            shl = shl.strip()
            self.subheadline = shl
        
    def _datetime(self):
        """Extract article date and time"""
        if self.article_soup is None:
            sess = requests.session()
            self._url()
            response = sess.get(self.url)
            self.article_soup = BeautifulSoup(response.text,
                                              "html.parser")
            # Find the elemet and ceate an iterator to separate
            # element strings between creation datetime and update datetime
            dt = list(self.article_soup.find(**constants_articles.datetime_element).stripped_strings)[0].split("-")
            # Select creation date by converting iterator into a list
            # and selecting the list first item.
            # Split the string into date and time
            # Select article date and remove trailing white spaces
            article_date = dt[0].strip()
            # Select article date and remove trailing white spaces
            article_time = dt[1].strip()
            # Parse date and time variables with dateparser
            string = f"{article_date} {article_time}"
            self.datetime = dateparser.parse((string))
            self.datetime = self.datetime.strftime('%Y-%m-%d %H:%M:%S') # type: ignore
        else:
            # Find the elemet and create an iterator to separate 
            # element strings between creation datetime and update datetime
            dt = list(self.article_soup.find(**constants_articles.datetime_element).stripped_strings)[0].split("-")
            # Select creation date by converting iterator into a list
            # and selecting the list first item.
            # Split the string into date and time
            # Select article date and remove trailing white spaces
            article_date = dt[0].strip()
            # Select article date and remove trailing white spaces
            article_time = dt[1].strip()
            # Parse date and time variables with dateparser
            datetime_string = f"{article_date} {article_time}"
            self.datetime = dateparser.parse((datetime_string))
            self.datetime = self.datetime.strftime('%Y-%m-%d %H:%M:%S') # type: ignore

    def _content(self):
        """Extract article body content"""
        if self.article_soup is None:
            sess = requests.session()
            self._url()
            response = sess.get(self.url)
            self.article_soup = BeautifulSoup(response.text,
                                              "html.parser")
            content_tag = self.article_soup.find_all(**constants_articles.content_element)

            content= []
            for __ in content_tag:
                content.append(__.text)
            self.content = " ".join(content)
        else:
            content_tag = self.article_soup.find_all(**constants_articles.content_element)

            content= []
            for __ in content_tag:
                content.append(__.text)
            self.content = " ".join(content)
    
    def construct_data_dict(self):
        
        self.get_hash()
        self._url()
        self._headline()
        self._author()
        self._subheadline()
        self._datetime()
        self._content()

        return {"hash": self.hash,
                "url": self.url,
                "headline": self.headline,
                "author": self.author,
                "subheadline": self.subheadline,
                "datetime": self.datetime,
                "content": self.content}
