import logging
import enlighten
import mysql.connector
import mysql.connector.abstracts 
from helpers import constants_querys as query
from helpers.constants_db import clever_cloud_db_credentials as credentials

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s :: %(module)s -> %(message)s')
logger = logging.getLogger(__name__)

class DBManager:
    """This is an object that performs database querys"""
    cursor: mysql.connector.abstracts.MySQLCursorAbstract    
    data: dict
    article_id: int
    locationid: int
    article_total: int
    score: float

    def __init__(self) -> None:
        """Object initialization"""
        logger.info("Initializing DBManager")
        

    def get_location_object(self) -> list:
        """
        Retrieve locations data from database
        
        :return: List of dictionaries with location NormalizedName and Name
        data
        :rtype: list
        """
        logger.info("Fetching locations")
        
        logger.info("Creating cursor object")
        dbconnection = mysql.connector.connect(**credentials)
        cursor = dbconnection.cursor(buffered=True)
        
        logger.info("Querying and fetching locations data")
        
        cursor.execute(query.RETRIEVE_LOCATIONS)
        result = cursor.fetchall()
        
        logger.info("Constructing data list")
        
        locationObj = []
        columnNames = [column[0] for column in cursor.description] # type: ignore
        record = ()
        for record in result:
            locationObj.append(dict(zip(columnNames, record)))
        
        logger.info("List created")

        logger.info("Closing cursor object")
        
        cursor.close()
        dbconnection.close()
        
        logger.info("Cursor closed")

        return locationObj

    def get_all_articles_object(self) -> list:
        """
        Retrieve all articles data from database
        
        :return: List of dictionaries with articles data
        :rtype: list
        """
        logger.info("Fetching articles data")
        
        logger.info("Creating cursor object")
        dbconnection = mysql.connector.connect(**credentials)
        cursor = dbconnection.cursor(buffered=True)
        
        logger.info("Querying and fetching articles data")
        
        cursor.execute(query.RETRIEVE_ALL_ARTICLES)
        result = cursor.fetchall()
        
        logger.info("Constructing data list")

        articlesObj = []
        columnNames = [column[0] for column in cursor.description] # type: ignore
        record = ()
        for record in result:
            articlesObj.append(dict(zip(columnNames, record)))
        
        logger.info("List created")

        logger.info("Closing cursor object")
        
        cursor.close()
        dbconnection.close()
        
        logger.info("Cursor closed")

        return articlesObj

    def _get_article_ids(self, location_id_dict: dict) -> tuple:
        """
        Private method to retrieve all article IDs with specified location
        id
        
        :return: Tuple of article ids
        :rtype: tuple
        """
        logger.info("Fetching article IDs")
        
        logger.info("Creating cursor object")
        dbconnection = mysql.connector.connect(**credentials)
        cursor = dbconnection.cursor(buffered=True)
        
        logger.info("Querying and fetching articles data")
        
        cursor.execute(query.RETRIEVE_ARTICLEID_FROM_LOCATIONID,
                       location_id_dict)
        result = cursor.fetchall()
        
        logger.info("Constructing data list")

        articleIDs = ()
        for rec in result:
            articleIDs = articleIDs + rec # type: ignore
        
        logger.info("List created")

        logger.info("Closing cursor object")
        
        cursor.close()
        dbconnection.close()
        
        logger.info("Cursor closed")

        return articleIDs
    
    def get_articles_from_location_object(self, location_id: int) -> list:
        """
        Retrieve all articles data specified location
        
        :return: List of dictionaries with articles data
        :rtype: list
        """
        logger.info("Fetching articles data from specified location")
        
        logger.info("Creating cursor object")
        dbconnection = mysql.connector.connect(**credentials)
        cursor = dbconnection.cursor(buffered=True)
        
        logger.info("Querying and fetching articles data")

        if location_id == 0:
            return self.get_all_articles_object()
        else:
            query_data = {"locationid": location_id}
            articleIDs = self._get_article_ids(location_id_dict=query_data)
            
            logger.info(articleIDs)
            
            if len(articleIDs) > 1:
                cursor.execute(f"""SELECT *
                            FROM Articles
                            WHERE ArticleID IN {articleIDs}
                            ORDER BY DateTime DESC
                            """)
            elif len(articleIDs) == 1:
                cursor.execute(f"""SELECT *
                            FROM Articles
                            WHERE ArticleID = {articleIDs[0]}
                            ORDER BY DateTime DESC
                            """)
            else:
                return []
            
            result = cursor.fetchall()
        
            logger.info("Constructing data list")

            articlesObj = []
            columnNames = [column[0] for column in cursor.description] # type: ignore
            record = ()
            for record in result:
                articlesObj.append(dict(zip(columnNames, record)))
            
            logger.info("List created")

            logger.info("Closing cursor object")
            
            cursor.close()
            dbconnection.close()
            
            logger.info("Cursor closed")

            return articlesObj