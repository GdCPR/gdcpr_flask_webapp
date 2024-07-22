INSERT_ARTICLE = """
INSERT INTO Articles (URL,
                      Headline,
                      Subheadline,
                      Author,
                      DateTime,
                      Hash)
VALUES (%(url)s, %(headline)s, %(author)s, %(subheadline)s, %(datetime)s, %(hash)s)
"""

INSERT_ARTICLE_LOCATION = """
INSERT INTO ArticlesLocationRelation (ArticleID,
                                      LocationID)
VALUES (%(articleid)s, %(locationid)s)
"""

FETCH_HASHES = """
SELECT Hash FROM Articles
"""