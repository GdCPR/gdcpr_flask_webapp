import os
import re
from flask import Flask, render_template, request, url_for, redirect
from helpers.manager_db import DBManager
import helpers.constants_querys as query
import json
# import logging

app_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(app_dir, "src", "templates")

app = Flask(__name__, template_folder=template_dir)

dbmanager = DBManager()
db = dbmanager.dbconnection


locationid = 2

locationObj = dbmanager.get_location_object()

articlesObj = dbmanager.get_articles_from_location_object(location_id=locationid)

print(articlesObj)

# # fetch articles id with specified locationid from bridge table
# cursor.execute(query.RETRIEVE_ARTICLEID_FROM_LOCATIONID, locationid)
# result = cursor.fetchall()
# articleIDs = ()
# for rec in result:
#     articleIDs = articleIDs + rec
# print(articleIDs)

# if articleIDs:
#     # Fetch Articles
#     cursor.execute(f"""SELECT * FROM Articles WHERE ArticleID IN {articleIDs} ORDER BY DateTime DESC""")
#     result = cursor.fetchall()
#     # Convertir datos a dict
#     articlesObj = []
#     columnNames = [column[0] for column in cursor.description] # type: ignore
#     record = ()
#     for record in result:
#         articlesObj.append(dict(zip(columnNames, record)))
#         print(record)
# else:
#     print("No articles for selected location!")

# cursor.close()
