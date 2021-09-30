from flask import Flask, request, render_template
from surveys import Question, Survey, satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)

responses = []

@app.route("/")
def home_page():
    """Shows home page."""

    return render_template("base.html", survey=satisfaction_survey)

@app.route("/questions/<int:id>")
def form(id):
    """Shows survey page."""

    return render_template("form.html", id=id)