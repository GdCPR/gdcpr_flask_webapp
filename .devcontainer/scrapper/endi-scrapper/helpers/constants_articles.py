BASE_URL = "https://www.elnuevodia.com"
URL = f"{BASE_URL}/noticias/seguridad"

arts_tag = "article"
arts_attrs = {"class": "standard-teaser-container condensed-horizontal news"}
articles_element = {"name": arts_tag,
                    "attrs": arts_attrs}

hl_tag = "h3"
hl_attrs = {"class": "standard-teaser-headline teaser-headline"}
headline_element = {"name": hl_tag,
                    "attrs": hl_attrs}

url_tag = "a"
url_element = {"name": url_tag,
               "href": True}

author_tag = "div"
author_class = {"class": "authors-byline-text"}
author_element = {"name": author_tag,
                  "attrs": author_class}

subheadline_tag = "div"
subheadline_class = {"class": "article-headline__subheadline"}
subheadline_element = {"name": subheadline_tag,
                       "attrs": subheadline_class}

datetime_tag = "div"
datetime_class = {"class": "article-headline__date"}
datetime_element = {"name": datetime_tag,
                    "attrs": datetime_class}

content_tag = "p"
content_class = {"class": "content-element"}
content_element = {"name": content_tag,
                   "attrs": content_class}