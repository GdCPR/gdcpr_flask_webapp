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
import csv
from db_connector import dbconnection as db

cursor = db.cursor(buffered=True)

ARTS_TB = "Articles"
LOC_TB = "Location"
ARTS_LOC_REL_TB = "ArticlesLocationRelation"

logging.basicConfig(level=logging.WARNING, format='%(levelname)s %(message)s')

####################################################################################
####################################################################################
# logging.warning("   Disabling  strict SQL mode")

# query = """SET GLOBAL sql_mode=''"""
# cursor.execute(query)

####################################################################################
####################################################################################
cursor.execute("""SHOW TABLES LIKE 'Articles'""") # Check if articles table exists
if len([row[0] for row in cursor]) == 0: # articles table no exists, create schema
   
  logging.warning("   Removing tables: %s, %s, %s",
                  ARTS_TB, LOC_TB, ARTS_LOC_REL_TB)

  # logging.warning(f"    [{datetime.now()}]    Removing tables: {ARTS_TB}, {LOC_TB}, {ARTS_LOC_TB}")

  query = f"""DROP TABLE IF EXISTS {ARTS_TB}, {LOC_TB}, {ARTS_LOC_REL_TB}"""
  cursor.execute(query)

  logging.warning("   Tables removed!")

  ####################################################################################
  ####################################################################################

  logging.warning("   Creating table: %s", ARTS_TB)
  # Query: Create Articles table
  create_artsTb_query = f"""
  CREATE TABLE IF NOT EXISTS {ARTS_TB} (
                                      ArticleID INTEGER AUTO_INCREMENT,
                                      URL VARCHAR(1024) NOT NULL, 
                                      Headline VARCHAR(1024) NOT NULL,
                                      Subheadline VARCHAR(1024) NOT NULL,
                                      Author VARCHAR(255) NOT NULL,
                                      DateTime DATETIME,
                                      Hash VARCHAR(512) NOT NULL,
                                      PRIMARY KEY (ArticleID)
                                      )
  """
  cursor.execute(create_artsTb_query)
  logging.warning("   **Table created**")

  ####################################################################################
  ####################################################################################

  dirname = os.path.dirname(__file__)
  filepath = os.path.join(dirname, "assets/puerto_rico_municipalities.txt")

  with open(filepath, mode ='r')as file:
    csvFile = csv.reader(file)
    # name = [municipality[0] for municipality in csvFile]
    locations = [[municipality[0], unidecode(municipality[1])] for municipality in csvFile]

  # name.sort()
  locations.sort()

  logging.warning("   Creating table: %s", LOC_TB)
  # Query: Create Location table
  create_locTb_query = f"""
  CREATE TABLE IF NOT EXISTS {LOC_TB} (
                                      LocationID INTEGER AUTO_INCREMENT,
                                      Name VARCHAR(255),
                                      NormalizedName VARCHAR(255),
                                      RelevanceScore DOUBLE DEFAULT 0,
                                      PRIMARY KEY (LocationID)
                                      )
  """
  cursor.execute(create_locTb_query)

  logging.warning("   Inserting data into Location table")
  query = """INSERT INTO Location (Name, NormalizedName) VALUES (%(Name)s, %(NormalizedName)s)"""
  for loc in locations:
      print(loc)
      data = {"Name": loc[0], "NormalizedName": loc[1]}
      cursor.execute(query, data)

  logging.warning("   **Table created**")

  ####################################################################################
  ####################################################################################

  logging.warning("   Creating table: %s", ARTS_LOC_REL_TB)
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
  logging.warning("   **Table created**")
  ####################################################################################
  ####################################################################################

  logging.warning("   Schema cleaned and ready!")

else:
   logging.warning("   Schema already exists and ready!")

db.commit()
db.close()
