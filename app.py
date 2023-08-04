from flask import Flask, request, jsonify, render_template

from query import respond_to_query



app = Flask(__name__)



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/answer")
def answer():
    return "<p>Hello, World!</p>"