"""
#####################################################################
#####################################################################

This file must be run only and only if you are trying to start a
clean schema with empty tables, or if you want to set up the schema
for the first time!

#####################################################################
#####################################################################
"""
import os
import logging
from datetime import datetime
from unidecode import unidecode
import pandas as pd
from database_connector import dbconnection as db

cursor = db.cursor(buffered=True)

ARTS_TB = "Articles"
LOC_TB = "Location"
ARTS_LOC_REL_TB = "ArticlesLocationRelation"

####################################################################################
####################################################################################
logging.warning("    [%s]    Disabling  strict SQL mode", datetime.now())

query = """SET GLOBAL sql_mode=''"""
cursor.execute(query)

####################################################################################
####################################################################################

logging.warning("    [%s]    Removing tables: %s, %s, %s",
                datetime.now() ,ARTS_TB, LOC_TB, ARTS_LOC_REL_TB)

# logging.warning(f"    [{datetime.now()}]    Removing tables: {ARTS_TB}, {LOC_TB}, {ARTS_LOC_TB}")

query = f"""DROP TABLE IF EXISTS {ARTS_TB}, {LOC_TB}, {ARTS_LOC_REL_TB}"""
cursor.execute(query)

logging.warning("    [%s]    Tables removed!", datetime.now())

####################################################################################
####################################################################################

logging.warning("    [%s]    Creating table: %s", datetime.now(), ARTS_TB)
# Query: Create Articles table
create_artsTb_query = f"""
CREATE TABLE IF NOT EXISTS {ARTS_TB} (
                                    ArticleID INTEGER AUTO_INCREMENT,
                                    URL VARCHAR(1024) NOT NULL, 
                                    Headline VARCHAR(1024) NOT NULL,
                                    Subheadline VARCHAR(1024) NOT NULL,
                                    Author VARCHAR(1024) NOT NULL,
                                    DateTime DATETIME,
                                    Hash VARCHAR(1024) NOT NULL,
                                    PRIMARY KEY (ArticleID)
                                    )
"""
cursor.execute(create_artsTb_query)
logging.warning("    [%s]    **Table created**", datetime.now())

####################################################################################
####################################################################################

dirname = os.path.dirname(__file__)
filepath = os.path.join(dirname, "resources/puerto_rico_municipalities.txt")
municipalities_df = pd.read_csv(filepath,
                                sep=" ",
                                header=None,
                                names=["municipality"])
# Filter for the first table and unique values from the Pueblos Column
municipalities_list = [unidecode(municipality)
                       for municipality in municipalities_df["municipality"].values]
municipalities_list.sort()

logging.warning("    [%s]    Creating table: %s", datetime.now(), LOC_TB)
# Query: Create Location table
create_locTb_query = f"""
CREATE TABLE IF NOT EXISTS {LOC_TB} (
                                    LocationID INTEGER AUTO_INCREMENT,
                                    Name VARCHAR(1024),
                                    PRIMARY KEY (LocationID)
                                    )
"""
cursor.execute(create_locTb_query)

logging.warning("    [%s]    Inserting data into Location table", datetime.now())
query = """INSERT INTO Location (Name) VALUES (%(Name)s)"""
for loc in municipalities_list:
    data = {"Name": loc}
    cursor.execute(query, data)

logging.warning("    [%s]    **Table created**", datetime.now())

####################################################################################
####################################################################################

logging.warning("    [%s]    Creating table: %s", datetime.now(), ARTS_LOC_REL_TB)
# Query: Create Article-Location Bridge table
create_artslocrelTB_query = f"""
CREATE TABLE IF NOT EXISTS {ARTS_LOC_REL_TB} (
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
####################################################################################
####################################################################################

logging.warning("    [%s]    Schema cleaned and ready!", datetime.now())

db.commit()
db.close()
