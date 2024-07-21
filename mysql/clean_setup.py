import database_connector as db

cursor = db.dbconnection.cursor(buffered=True)

# db schema is empty and can start being configured