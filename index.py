from flask import Flask, render_template, request, url_for, redirect
import mysql.connector

app = Flask(__name__)

def conn_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="P@ssw0rd",
        db="HALcinema"
    )
    return conn

if __name__ == "__main__":
    app.run(host="localhost",port=8000,debug=True)