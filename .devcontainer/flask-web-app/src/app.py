import os
from flask import Flask, render_template, request, url_for, redirect, jsonify
from helpers.manager_db import DBManager
# import logging

app_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(app_dir, "src", "templates")

app = Flask(__name__, template_folder=template_dir)

dbmanager = DBManager()
db = dbmanager.dbconnection

# Rutas de la aplicación
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        location = request.form['location']
        if location:
            return jsonify({'output': f"The selected location is: {location}"})
        return jsonify({'error' : 'Error!'})

    db.reconnect()
    cursor = db.cursor(buffered=True)

    # Fetch Locations
    cursor.execute("""SELECT LocationID, NormalizedName, Name FROM Location ORDER BY LocationID""")
    result = cursor.fetchall()
    locationObj = []
    columnNames = [column[0] for column in cursor.description] # type: ignore
    for record in result:
        locationObj.append(dict(zip(columnNames, record)))

    # Fetch Articles
    cursor.execute("""SELECT * FROM Articles ORDER BY DateTime DESC""")
    result = cursor.fetchall()
    # Convertir datos a dict
    articlesObj = []
    columnNames = [column[0] for column in cursor.description] # type: ignore
    for record in result:
        articlesObj.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template("index.html",
                           articles=articlesObj,
                           location=locationObj)

if __name__ == "__main__":
    app.run(debug=True, port=4327)