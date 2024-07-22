INSERT_ARTICLE = """
INSERT INTO Articles (URL,
                      Headline,
                      Subheadline,
                      Author,
                      DateTime)
VALUES (%(url)s, %(headline)s, %(author)s, %(subheadline)s, %(datetime)s)
"""
