import mysql.connector

from config import DB_USER_PASS


CONNECTION = mysql.connector.connect(
    host='localhost',
    user='',
    passwd=DB_USER_PASS,
    database='support_db'
)


def query():
    pass
