import mysql.connector
from credentials import clever_cloud_db_credentials as credentials

dbconnection = mysql.connector.connect(**credentials)
