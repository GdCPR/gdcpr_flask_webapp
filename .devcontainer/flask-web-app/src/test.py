from helpers.manager_db import DBManager

dbmanager = DBManager()
db = dbmanager.dbconnection

db.reconnect()
cursor = db.cursor(buffered=True)

# Fetch Locations
cursor.execute("""SELECT NormalizedName, Name FROM Location ORDER BY LocationID""")
result = cursor.fetchall()
locationObj = []
columnNames = [column[0] for column in cursor.description]
for record in result:
    locationObj.append(dict(zip(columnNames, record)))

cursor.close()
db.close()

print(locationObj)