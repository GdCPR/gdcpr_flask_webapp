INSERT_ARTICLE = """
INSERT INTO Articles 
(URL, Headline, Subheadline, Author, DateTime, Hash)
VALUES (%(url)s, %(headline)s, %(subheadline)s, %(author)s, %(datetime)s, %(hash)s)
"""

INSERT_ARTICLE_LOCATION = """
INSERT INTO ArticlesLocationRelation
(ArticleID, LocationID)
VALUES (%(articleid)s, %(locationid)s)
"""

UPDATE_RELEVACE_SCORE = """
UPDATE Location
SET RelevanceScore = %(score)s
WHERE LocationID = %(locationid)s;
"""

FETCH_HASHES = """
SELECT Hash 
FROM Articles
"""

COUNT = """
SELECT COUNT(*) 
FROM ArticlesLocationRelation 
WHERE LocationID = %(locationid)s
"""

ARTICLE_MAXID = """
SELECT *
FROM Articles
ORDER BY ArticleID
DESC LIMIT 1
"""

CHECK_HASH = """
SELECT Hash, 
COUNT(*) FROM Articles
WHERE Hash = %s
GROUP BY Hash
"""
