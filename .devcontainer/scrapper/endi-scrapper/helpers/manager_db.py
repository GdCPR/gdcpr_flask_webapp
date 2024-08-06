import logging
import mysql.connector
import mysql.connector.abstracts 
from helpers import constants_querys as query
from helpers.constants_db import clever_cloud_db_credentials as credentials

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s :: %(module)s -> %(message)s')
logger = logging.getLogger(__name__)

class DBManager:

    cursor: mysql.connector.abstracts.MySQLCursorAbstract    
    data: dict
    article_id: int
    locationid: int
    article_total: int
    score: float

    def __init__(self) -> None:

        logger.info("Initializing DBManager")
        self.dbconnection = mysql.connector.connect(**credentials)
        self.cursor = self.dbconnection.cursor(buffered=True)

    def _validate_location(self) -> bool:
        
        logging.info("Validating article location")

        self.cursor.execute(query.FETCH_NORMALIZED_NAME)
        normalized_loc_name = self.cursor.fetchall()

        official_loc = [row[0] for row in normalized_loc_name] # type: ignore

        validated_loc = set(self.data["location"]) & set(official_loc)

        self.data["valid_loc"] = validated_loc

        return True if validated_loc else False

    def _get_location_id(self, location: str) -> None:
        logging.info("Getting location ID")

        self.cursor.execute(query.FETCH_NORMALIZED_NAME_ID,
                            {"validated_location": location})
        
        for row in self.cursor.fetchall():
            if location == row[1]: # type: ignore
                self.locationid = row[0] # type: ignore

        logging.info(f"Location: {location}, ID: {self.locationid}")

    def _insert_bridge_tb(self) -> None:
        logging.info("Inserting in Bridge Table")

        self.cursor.execute(query.INSERT_ARTICLE_LOCATION_RELATION,
                            {"articleid": self.data["articleid"],
                             "locationid": self.locationid}) # type: ignore

        self.dbconnection.commit()

    def _get_total_articles(self) -> None:

        self.cursor.execute(query.ARTICLE_MAXID)
        self.article_total = int(self.cursor.fetchone()[0])  # type: ignore

    def _calculate_relevance_score(self):
        logging.info("Calculating Relevance Score")

        self.cursor.execute(query.COUNT,
                            {"locationid": self.locationid}) # type: ignore
        loc_count = int(self.cursor.fetchone()[0]) # type: ignore

        self.score = loc_count/self.article_total

    def _insert_relevance_score(self) -> None:
        logging.info("Updating Relevance Score")

        self._get_total_articles()
        self.cursor.execute(query.FETCH_LOCATION_ID)
        for row in self.cursor.fetchall(): # type: ignore
                self.locationid = row[0] # type: ignore
                self._calculate_relevance_score()
                self.cursor.execute(query.UPDATE_RELEVACE_SCORE,
                                    {"locationid": self.locationid,
                                     "score": self.score}) # type: ignore
                self.dbconnection.commit()
    
    def _insert_article_data(self) -> None:
        logging.info("Inserting Article Data")

        tmp_data_dict = self.data.copy()
        tmp_data_dict.pop("location")
        self.cursor.execute(query.INSERT_ARTICLE, tmp_data_dict)
        self.dbconnection.commit()
        self.data["articleid"] = self.cursor.lastrowid # type: ignore

    def check_hash(self, article_hash: dict) -> bool:

        logging.info("Checking article hash")
        
        self.cursor.execute(query.CHECK_HASH, article_hash)
        check = self.cursor.rowcount

        return True if check else False

    def write_in_tables(self, data: dict) -> None:
        self.data = data

        self._insert_article_data()
        
        if self._validate_location():
            for loc in self.data["valid_loc"]:
                self._get_location_id(location=loc)
                self._insert_bridge_tb()
    
        self._insert_relevance_score()

        self.cursor.close()
        self.dbconnection.close()