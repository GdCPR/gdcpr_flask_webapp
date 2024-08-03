from helpers.manager_articles import current_articles, Article

articles = current_articles()

for article in articles:

    article = Article(article= article)

    print(article._author())