RETRIEVE_LOCATIONS = """
SELECT LocationID, NormalizedName, Name
FROM Location
ORDER BY LocationID
"""

RETRIEVE_ALL_ARTICLES = """
SELECT *
FROM Articles
ORDER BY DateTime DESC
"""

RETRIEVE_ARTICLEID_FROM_LOCATIONID = """
SELECT ArticleID
FROM ArticlesLocationRelation
WHERE LocationID = %(locationid)s
"""