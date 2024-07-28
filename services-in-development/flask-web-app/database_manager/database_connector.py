import mysql.connector
from database_manager.credentials import clever_cloud_db_credentials as credentials

dbconnection = mysql.connector.connect(**credentials)
