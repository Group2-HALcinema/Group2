import mysql.connector

def conn_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="P@ssw0rd",
        db="HALcinema"
    )
    return conn