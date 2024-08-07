import logging
import enlighten
import mysql.connector
import mysql.connector.abstracts 
# from helpers import constants_querys as query
from helpers.constants_db import clever_cloud_db_credentials as credentials

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s :: %(module)s -> %(message)s')
logger = logging.getLogger(__name__)

class DBManager:
    """This is an object that performs database querys and manipulation"""
    cursor: mysql.connector.abstracts.MySQLCursorAbstract    
    data: dict
    article_id: int
    locationid: int
    article_total: int
    score: float

    def __init__(self) -> None:
        """Object initialization"""
        logger.info("Initializing DBManager")
        
        self.dbconnection = mysql.connector.connect(**credentials)

        logger.info("Creating cursor object")

        self.cursor = self.dbconnection.cursor(buffered=True)

    def _validate_location(self) -> bool:
        """
        Validate location found in article with official locations list
        
        :return: True or False based if location found is in official
        location list
        :rtype: bool 
        """
        logger.info("Validating article location")

        self.cursor.execute(query.FETCH_NORMALIZED_NAME)
        normalized_loc_name = self.cursor.fetchall()
        official_loc = [row[0] for row in normalized_loc_name] # type: ignore
        validated_loc = set(self.data["location"]) & set(official_loc)
        self.data["valid_loc"] = validated_loc

        logger.info(f"Official location? {True if validated_loc else False}")

        return True if validated_loc else False

    def _get_location_id(self, location: str) -> None:
        """
        Fetch location id from database

        :param location: Location to check in database
        :type location: str
        """
        logger.info("Getting location ID")

        self.cursor.execute(query.FETCH_NORMALIZED_NAME_ID,
                            {"validated_location": location})
        
        for row in self.cursor.fetchall():
            if location == row[1]: # type: ignore
                self.locationid = row[0] # type: ignore

        logger.info(f"Location: {location}")
        logger.info(f"ID: {self.locationid}")

    def _insert_bridge_tb(self) -> None:
        """Insert Article-Location relation in database"""
        logger.info("Inserting data in bridge table")

        self.cursor.execute(query.INSERT_ARTICLE_LOCATION_RELATION,
                            {"articleid": self.data["articleid"],
                             "locationid": self.locationid}) # type: ignore

        self.dbconnection.commit()

        logger.info(f"Article id: {self.data["articleid"]}")
        logger.info(f"Location id: {self.locationid}")

    def _get_total_articles(self) -> None:
        """Fetch total articles in database"""
        logger.info("Fetching total articles in database")

        self.cursor.execute(query.ARTICLE_MAXID)
        self.article_total = int(self.cursor.fetchone()[0])  # type: ignore

        logger.info(f"Total articles: {self.article_total}")

    def _calculate_relevance_score(self):
        """Calculate location relevance score"""
        # logger.info("Calculating Relevance Score")

        self.cursor.execute(query.COUNT,
                            {"locationid": self.locationid}) # type: ignore
        loc_count = int(self.cursor.fetchone()[0]) # type: ignore

        self.score = loc_count/self.article_total

        # logger.info(f"Relevance score: {self.score}")

    def _insert_relevance_score(self) -> None:
        """Update location relevance score in database"""
        logger.info("Updating Relevance Score")

        self._get_total_articles()
        self.cursor.execute(query.FETCH_LOCATION_ID)

        # Create progress bar manager handler
        manager = enlighten.get_manager()
        # Create basic progress bar
        pbar = manager.counter(desc='Progress', unit='ticks')
        
        for row in self.cursor.fetchall(): # type: ignore
                self.locationid = row[0] # type: ignore
                self._calculate_relevance_score()
                self.cursor.execute(query.UPDATE_RELEVACE_SCORE,
                                    {"locationid": self.locationid,
                                     "score": self.score}) # type: ignore
                self.dbconnection.commit()
                pbar.update()

        logger.info(f"Rrelevance scores successfully updated")
        
        manager.stop()
    
    def _insert_article_data(self) -> None:
        """Insert article data in database"""
        logger.info("Inserting article data")

        tmp_data_dict = self.data.copy()
        tmp_data_dict.pop("location")
        self.cursor.execute(query.INSERT_ARTICLE, tmp_data_dict)
        self.dbconnection.commit()
        self.data["articleid"] = self.cursor.lastrowid # type: ignore

        logger.info("Article data successfully inserted")

    def check_hash(self, article_hash: dict) -> bool:
        """Check article hash exists in database"""
        logger.info("Checking article hash")
        
        self.cursor.execute(query.CHECK_HASH, article_hash)
        check = self.cursor.rowcount

        logger.info(f"Article exixts in database? {True if check else False}")

        return True if check else False

    def write_in_tables(self, data: dict) -> None:
        """
        Executes private methods to insert article data in database, validate
        location found, insert article-location relation, and update relevance
        score

        :param data: Article data
        :type data: dict
        """
        self.data = data

        self._insert_article_data()
        
        if self._validate_location():
            for loc in self.data["valid_loc"]:
                self._get_location_id(location=loc)
                self._insert_bridge_tb()
    
        self._insert_relevance_score()

        self.cursor.close()
        self.dbconnection.close()