import mysql.connector


def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="shruthyy@66",
        database="internship_portal"
    )