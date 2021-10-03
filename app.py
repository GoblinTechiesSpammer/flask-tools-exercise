from flask import Flask, request, render_template, flash, session
from flask.json import jsonify
from werkzeug.utils import redirect
from surveys import Question, Survey, satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)

# responses = []

@app.route("/")
def home_page():
    """Shows home page."""

    return render_template("base.html", survey=satisfaction_survey)

@app.route("/questions/<int:id>")
def form(id):
    """Shows survey page."""

    #Prevents wrong question id from being manually entered in the address bar.
    if id > len(session['responses']):
        flash('Invalid Question!')
        return redirect(f"/questions/{len(session['responses'])}")

    return render_template("form.html", question=satisfaction_survey.questions[id])

@app.route("/answer", methods=["POST"])
def answer():
    """Post request to next survey question"""

    choice = request.form["answer"]

    #Append the choice to responses, but in a weird way for session to work, instead of just session['responses'].append(choice)
    responses = session['responses']
    responses.append(choice)
    session['responses'] = responses

    next_question_id = len(session['responses'])

    #Redirect to completion page when questions run out.
    if len(session['responses']) == len(satisfaction_survey.questions):
        return redirect("/complete")

    return redirect(f"/questions/{next_question_id}")   #Cannot format url like @app.route variable format

@app.route("/complete")
def complete():
    """Shows the end of survey page."""

    return render_template("complete.html")

@app.route("/session", methods=["POST"])
def session_store():
    # Empty the response list to start from a clean slate.
    session['responses'] = []

    return redirect("/questions/0")