from helpers.manager_articles import current_articles, Article

articles = current_articles()

for article in articles:

    article = Article(article_tag= article)

    print(article._content())