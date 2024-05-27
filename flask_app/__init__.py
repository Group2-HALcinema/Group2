from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

if __name__ == "__main__":
    app.run(host="localhost",port=8000,debug=True)