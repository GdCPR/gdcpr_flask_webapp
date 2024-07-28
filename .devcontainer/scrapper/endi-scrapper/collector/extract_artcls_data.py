import requests
import dateparser
from bs4 import BeautifulSoup, element
from collector.art_hash import get_hash

####################################################################
####################################################################
# Add more explicit description than doctring
####################################################################
####################################################################
def current_artcls(news_url):
    """
    Extract current articles from url.

    """
    # Get request to base url
    s = requests.Session()
    news_html = s.get(news_url)

    # Creating soup of HTML text content with bs4 HTML parser
    main_soup = BeautifulSoup(news_html.text,
                             'html.parser')

    # Find all articles by tag and class specification
    articles= main_soup.find_all('article',
                                 {'class': 'standard-teaser-container condensed-horizontal news'})

    return articles
####################################################################
####################################################################
# Add more explicit description than doctring
####################################################################
####################################################################
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
    # Get article hash
    hash = get_hash(article=article)

    # Extract article title
    # Create an iterator to separate headline from subheadline
    html_attrs_dict = {'class':'standard-teaser-headline teaser-headline'}
    headline_iterator = article.find(name='h3',
                                        attrs=html_attrs_dict).stripped_strings # type: ignore
    # Fetch the first item only which corresponds to the headline
    article_headline = next(headline_iterator)

    # Extract article path
    article_path = article.find(name="a",
                                href=True)['href'] # type: ignore
    # Create article full url
    article_url = f"https://www.elnuevodia.com{article_path}".format(article_path)

    # Extract article author
    html_attrs_dict = {"class": "authors-byline-text"}
    article_author = article.find(name="div",
                                    attrs=html_attrs_dict).text.strip() # type: ignore

    # Return dictionary with data
    return {"url": article_url,
            "headline": article_headline,
            "author": article_author,
            "hash": hash}

####################################################################
####################################################################
# Add more explicit description than doctring
####################################################################
####################################################################
def artcl_content(article_data: dict) -> dict:
    """
    Should return a dictionary with articles content to save
    """
    s = requests.Session()
    article_html = s.get(article_data["url"])

    article_soup = BeautifulSoup(article_html.text,
                                "html.parser")
    html_attrs_dict = {"class": "article-headline__subheadline"}
    headline_sub = article_soup.find(name="div",
                                     attrs=html_attrs_dict).text.strip() # type: ignore

    # Extract date and time
    # Create an iterator to separate string if there was an update annotation
    # Convert iterator in a list and split string
    html_attrs_dict = {"class": "article-headline__date"}
    article_date_time_list = list(article_soup.find(name= "div",
                                                    attrs=html_attrs_dict
                                                    ).stripped_strings)[0].split("-") # type: ignore
    # Save date and time in separated variables
    article_date = article_date_time_list[0].strip()
    article_time = article_date_time_list[1].strip()
    # Parse date and time variables with dateparser
    article_date_time = dateparser.parse((f"{article_date} {article_time}"
                                         ).format(article_date, article_time))

    article_content = article_soup.find_all(name="p",
                                            attrs={"class": "content-element"})
    content= []
    for __ in article_content:
        content.append(__.text)
    content = " ".join(content)

    return {"subheadline": headline_sub,
            "datetime": article_date_time.strftime('%Y-%m-%d %H:%M:%S'),
            "content": content}
