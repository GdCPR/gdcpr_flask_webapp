import mysql.connector

dbparameters = {"host": "database",
                "user": "root",
                "password": "root",
                "database": "db",
                "port": 3306}

dbconnection = mysql.connector.connect(host=dbparameters["host"],
                                       user=dbparameters["user"],
                                       password=dbparameters["password"],
                                       database=dbparameters["database"],
                                       port=dbparameters["port"])
