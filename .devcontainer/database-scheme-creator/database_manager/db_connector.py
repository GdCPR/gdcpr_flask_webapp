import mysql.connector
# from credentials import container_db_credentials as credentials
from credentials import clever_cloud_db_credentials as credentials

dbconnection = mysql.connector.connect(**credentials)
