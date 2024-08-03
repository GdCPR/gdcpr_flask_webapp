BASE_URL = "https://www.elnuevodia.com"
URL = f"{BASE_URL}/noticias/seguridad"

arts_name = "article"
arts_attrs = {"class": "standard-teaser-container condensed-horizontal news"}
articles_element = {"name": arts_name,
                    "attrs": arts_attrs}

hl_name = "h3"
hl_attrs = {"class": "standard-teaser-headline teaser-headline"}
headline_element = {"name": hl_name,
                    "attrs": hl_attrs}

url_name = "a"
url_element = {"name": url_name,
               "href": True}

author_name = "div"
author_class = {"class": "authors-byline-text"}
author_element = {"name": author_name,
                  "attrs": author_class}