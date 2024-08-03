from helpers.manager_articles import current_articles, Article
from helpers.manager_db import DBConsultor

articles_result_set = current_articles()
dbconsultor = DBConsultor()

for article_tag in articles_result_set:

    article = Article(tag = article_tag)

    if dbconsultor.check_hash(article.get_hash()):
        article_data_dict = article.construct_data_dict()
        print("Article Exists")
    else:
        print("Don't Exists")