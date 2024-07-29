import os
from flask import Flask, render_template
from database_manager.database_connector import dbconnection as db

app_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(app_dir, "src", "templates")

app = Flask(__name__, template_folder=template_dir)


# Rutas de la aplicación
@app.route("/")
def home():


    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True, port=4327)