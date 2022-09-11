from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

responses_key = "responses"

app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def start_page():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('survey.html', title=title, instructions=instructions)

@app.route('/questions/<int:num>')
def question_page(num):

    responses = session.get(responses_key)

    if (responses is None):
        return redirect('/')
    if num != len(responses):
        flash('Invalid question')
        return redirect(f'/questions/{len(responses)}')
    question_list = satisfaction_survey.questions
    question = question_list[num]
    if num == len(question_list):
        return render_template('thank_you.html')
    return render_template('question.html', question=question, num=num)

@app.route('/answer', methods=['POST'])
def answer_page():

    response = request.form['answer']

    responses = session[responses_key]
    responses.append(response)
    session[responses_key] = responses

    list_len = len(responses)
    question_list = satisfaction_survey.questions
    if list_len == len(question_list):
        return redirect('/thank_you')
    return redirect(f"/questions/{list_len}")

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/reset', methods = ['POST'])
def reset_responses_list():
    session[responses_key] = []
    return redirect('/questions/0')