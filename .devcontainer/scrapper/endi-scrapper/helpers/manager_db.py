import mysql.connector
from constants_db import clever_cloud_db_credentials as credentials
import constants_querys as query

class DBConsultor:
    def __init__(self) -> None:
        self.dbconnection = mysql.connector.connect(**credentials)

    def check_hash(self, article_hash: dict) -> bool:
        self.dbconnection.reconnect()
        cursor = self.dbconnection.cursor()
        cursor.execute(query.CHECK_HASH, article_hash)
        check = cursor.rowcount
        return True if check else False
