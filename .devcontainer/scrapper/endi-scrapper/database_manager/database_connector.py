import mysql.connector
from database_manager.credentials import clever_cloud_db_credentials as creds

dbconnection = mysql.connector.connect(**creds)
