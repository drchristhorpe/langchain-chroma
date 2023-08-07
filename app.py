from flask import Flask, request, jsonify, render_template

from query_content import respond_to_query

app = Flask(__name__)



@app.route("/")
def home():
    return render_template("onepage.html")


@app.route("/answer")
def answer():
    question = request.args.get('question')
    if question:
        question = question.strip().replace('?','')
        answer = respond_to_query(question)
    else:
        answer = None
    return render_template("onepage.html", answer=answer, question=question)