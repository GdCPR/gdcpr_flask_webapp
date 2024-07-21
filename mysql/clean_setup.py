"""
#####################################################################
#####################################################################

This file must be run only and only if you are trying to start a
clean schema with empty tables, or if you want to set up the schema
for the first time!

#####################################################################
#####################################################################
"""
import logging
from datetime import datetime
from database_connector import dbconnection as db

cursor = db.cursor(buffered=True)

ARTS_TB = "Articles"
LOC_TB = "Location"
ARTS_LOC_TB = "ArticlesLocationRelation"

logging.warning("    [%s]    Removing tables: %s, %s, %s",
                datetime.now() ,ARTS_TB, LOC_TB, ARTS_LOC_TB)

# logging.warning(f"    [{datetime.now()}]    Removing tables: {ARTS_TB}, {LOC_TB}, {ARTS_LOC_TB}")

query = f"""DROP TABLE IF EXISTS {ARTS_TB}, {LOC_TB}, {ARTS_LOC_TB}"""
cursor.execute(query)

logging.warning("    [%s]    Tables removed!", datetime.now())

logging.warning("    [%s]    Creating table: %s", datetime.now(), ARTS_TB)
# Query: Create Articles table
create_artsTb_query = f"""
CREATE TABLE IF NOT EXISTS {ARTS_TB} (
                                    ArticleID INTEGER,
                                    URL VARCHAR(1024) NOT NULL, 
                                    Headline VARCHAR(1024) NOT NULL,
                                    Subheadline VARCHAR(1024) NOT NULL,
                                    Author VARCHAR(1024) NOT NULL,
                                    DateTime DATETIME,
                                    PRIMARY KEY (ArticleID)
                                    )
"""
cursor.execute(create_artsTb_query)
logging.warning("    [%s]    **Table created**", datetime.now())

logging.warning("    [%s]    Creating table: %s", datetime.now(), LOC_TB)
# Query: Create Location table
create_locTb_query = f"""
CREATE TABLE IF NOT EXISTS {LOC_TB} (
                                    LocationID INTEGER,
                                    Name VARCHAR(1024),
                                    PRIMARY KEY (LocationID)
                                    )
"""
cursor.execute(create_locTb_query)
logging.warning("    [%s]    **Table created**", datetime.now())

logging.warning("    [%s]    Creating table: %s", datetime.now(), ARTS_LOC_TB)
# Query: Create Article-Location Bridge table
create_artslocrelTB_query = f"""
CREATE TABLE IF NOT EXISTS {ARTS_LOC_TB} (
                                            ArticleID INTEGER NOT NULL,
                                            LocationID INTEGER NOT NULL,
                                            FOREIGN KEY (ArticleID)
                                            REFERENCES {ARTS_TB}(ArticleID),
                                            FOREIGN KEY (LocationID)
                                            REFERENCES {LOC_TB}(LocationID),
                                            INDEX (ArticleID, LocationID),
                                            UNIQUE (ArticleID, LocationID)
                                            )
"""
cursor.execute(create_artslocrelTB_query)
logging.warning("    [%s]    **Table created**", datetime.now())

logging.warning("    [%s]    Schema cleaned and ready!", datetime.now())

db.commit()
