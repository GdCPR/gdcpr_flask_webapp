"""
#####################################################################
#####################################################################

This file must be run only and only if you are trying to start a
clean schema with empty tables, or if you want to set up the schema
for the first time!

#####################################################################
#####################################################################
"""
import database_connector as db
import logging
from datetime import datetime

cursor = db.dbconnection.cursor(buffered=True)

artsTB = "Articles"
locTB = "Location"
artslocrelTB = "ArticlesLocationRelation"

logging.warning(f"    [{datetime.now()}]    Removing tables: {artsTB}, {locTB}, {artslocrelTB}")

query = f"""DROP TABLE IF EXISTS {artsTB}, {locTB}, {artslocrelTB}"""
cursor.execute(query)

logging.warning(f"    [{datetime.now()}]    Tables removed!")

logging.warning(f"    [{datetime.now()}]    Creating table: {artsTB}")
# Query: Create Articles table
create_artsTb_query = f"""
CREATE TABLE IF NOT EXISTS {artsTB} (
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
logging.warning(f"    [{datetime.now()}]    **Table created**")

logging.warning(f"    [{datetime.now()}]    Creating table: {locTB}")
# Query: Create Location table
create_locTb_query = f"""
CREATE TABLE IF NOT EXISTS {locTB} (
                                    LocationID INTEGER,
                                    Name VARCHAR(1024),
                                    PRIMARY KEY (LocationID)
                                    )
"""
cursor.execute(create_locTb_query)
logging.warning(f"    [{datetime.now()}]    **Table created**")

logging.warning(f"    [{datetime.now()}]    Creating table: {artslocrelTB}")
# Query: Create Article-Location Bridge table
create_artslocrelTB_query = f"""
CREATE TABLE IF NOT EXISTS {artslocrelTB} (
                                            ArticleID INTEGER NOT NULL,
                                            LocationID INTEGER NOT NULL,
                                            FOREIGN KEY (ArticleID) REFERENCES {artsTB}(ArticleID),
                                            FOREIGN KEY (LocationID) REFERENCES {locTB}(LocationID),
                                            INDEX (ArticleID, LocationID),
                                            UNIQUE (ArticleID, LocationID)
                                            )
"""
cursor.execute(create_artslocrelTB_query)
logging.warning(f"    [{datetime.now()}]    **Table created**")

logging.warning(f"    [{datetime.now()}]    Schema cleaned and ready!")

db.dbconnection.commit()