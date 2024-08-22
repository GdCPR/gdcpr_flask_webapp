import os
from flask import Flask, render_template, request, url_for, redirect, jsonify
from helpers.manager_db import DBManager
# import logging

app_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(app_dir, "src", "templates")

app = Flask(__name__, template_folder=template_dir)

dbmanager = DBManager()

# Rutas de la aplicación
@app.route("/", methods=["GET", "POST"])
def index():
    # Checking if cliente user clicked a specific location
    # If true, then the page was already loaded and the client
    # wants to update table based on request
    # If false, then is the first time the page was loaded therefore
    # all articles and locations are sent 
    if request.method == "POST":
        locationid = request.form['location']
        if locationid:
            articlesObj = dbmanager.get_articles_from_location_object(int(locationid))
            return {'output': f"Client selected location with ID: {locationid}",
                    "articlesObj": articlesObj}
        return jsonify({'error' : 'Error!'})
    else:
        locationObj = dbmanager.get_location_object()
        articlesObj = dbmanager.get_all_articles_object()
        return render_template("index.html",
                        articles=articlesObj,
                        location=locationObj)

if __name__ == "__main__":
    app.run(debug=True, port=4327)