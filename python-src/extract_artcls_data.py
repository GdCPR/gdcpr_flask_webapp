import math
from langcodes import tag_is_valid
import requests
from bs4 import BeautifulSoup, element


def current_artcls(news_url):
    """
    Extract current articles from url.

    """
    # Get request to base url
    s = requests.Session()
    news_html= s.get(news_url)

    # Creating soup of HTML text content with bs4 HTML parser
    main_soup= BeautifulSoup(news_html.text,
                             'html.parser')

    # Find all articles by tag and class specification
    articles= main_soup.find_all('article',
                                 {'class': 'standard-teaser-container condensed-horizontal news'})

    return articles

def artcl_data(article: element.Tag) -> dict: # type: ignore
        """
        Extract articles headline, url, and author from endi.com digital newspaper.

        Parameters
        ----------
        articles : ResultSet
            list of query results

        Returns
        -------
        dict
            a dictionary containing article title, url, and author data

        Raises
        ------
        Error Counter
            when article not found
        """
        try:
            # Extract article title 
            # Create an iterator to separate headline from subheadline
            iterator= article.find(name= 'h3',
                                   attrs= {'class':'standard-teaser-headline teaser-headline'}).stripped_strings
            # Fetch the first item only which corresponds to the headline
            article_headline= next(iterator)

            
            # Extract article path
            article_path= article.find(name= "a",
                                       href= True)['href'] # type: ignore
            # Create article full url
            article_url= "https://www.elnuevodia.com{path}".format(path= article_path)
            
            # Extract article author
            article_author= article.find("div",
                                         {"class": "authors-byline-text"}).text # type: ignore
            
            # Return dictionary with data
            return {"headline": article_headline,
                    "url": article_url,
                    "author": article_author}
        except:
             # Print message is find error
             print("¡No se encontró resultado!")

def artcl_content(article_data: dict) -> dict:
    """
    """
    s = requests.Session()
    article_html = s.get(article_data["url"])
    
    article_soup= BeautifulSoup(article_html.text,
                                "html.parser")
    
    headline_sub= article_soup.find(name= "div",
                                    attrs= {"class": "article-headline__subheadline"}).text # type: ignore
    
    article_date_time= (article_soup.find(name= "div",
                                          attrs= {"class": "article-headline__date"}).text).split("-") # type: ignore
    article_date= article_date_time[0].strip()
    article_time= article_date_time[1].strip()
    
    article_content= article_soup.find_all(name= "p",
                                           attrs= {"class": "content-element"})
    content= []
    for __ in article_content: content.append(__.text)
    content= " ".join(content)
    
    return {"headline_sub": headline_sub,
            "date": article_date,
            "time": article_time,
            "content": content}