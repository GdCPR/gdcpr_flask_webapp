import os
from flask import Flask, render_template
from database_manager.database_connector import dbconnection as db

app_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(app_dir, "src", "templates")

app = Flask(__name__, template_folder=template_dir)


# Rutas de la aplicación
@app.route("/")
def home():
    db.reconnect()
    cursor = db.cursor(buffered=True)

    # Fetch Locations
    cursor.execute("""SELECT Name FROM Location ORDER BY LocationID""")
    result = cursor.fetchall()
    locationObj = []
    columnNames = [column[0] for column in cursor.description]
    for record in result:
        locationObj.append(dict(zip(columnNames, record)))

    # Fetch Articles
    cursor.execute("""SELECT * FROM Articles ORDER BY DateTime DESC""")
    result = cursor.fetchall()
    # Convertir datos a dict
    articlesObj = []
    columnNames = [column[0] for column in cursor.description]
    for record in result:
        articlesObj.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template("index.html",
                           articles=articlesObj,
                           location=locationObj)


if __name__ == "__main__":
    app.run(debug=True, port=4327)