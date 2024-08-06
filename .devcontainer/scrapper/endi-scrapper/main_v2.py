import logging
from helpers.manager_articles import current_articles, Article
from helpers.manager_db import DBManager

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s :: %(module)s -> %(message)s')
logger = logging.getLogger(__name__)

# Fetch current articles from endi.com
articles_result_set = current_articles()

for article_tag in articles_result_set:

    # Initialize article manager
    article = Article(tag = article_tag)

    # Initialize database manager
    dbconsultor = DBManager()


    if dbconsultor.check_hash(article.get_hash()):
        print("Article Exists")
        article_data_dict = article.construct_data_dict()
        # print(article_data_dict)
        # dbconsultor.write_in_tables(article_data_dict)

    else:
        print("Don't Exists")
        article_data_dict = article.construct_data_dict()
        # print(article_data_dict)
        # dbconsultor.write_in_tables(article_data_dict)