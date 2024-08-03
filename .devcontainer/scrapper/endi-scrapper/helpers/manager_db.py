import mysql.connector
from helpers import constants_querys as query
from helpers.constants_db import clever_cloud_db_credentials as credentials

class DBConsultor:
    def __init__(self) -> None:
        self.dbconnection = mysql.connector.connect(**credentials)

    def check_hash(self, article_hash: dict) -> bool:
        self.dbconnection.reconnect()
        cursor = self.dbconnection.cursor(buffered=True)
        cursor.execute(query.CHECK_HASH, article_hash)
        check = cursor.rowcount
        return True if check else False
    
    def get_article_id(self):
        pass
    
    def insert_article_tb(self):
        pass

    def insert_location_tb(self):
        pass

    def insert_bridge_tb(self):
        pass

    def insert_relevance_score(self):
        pass