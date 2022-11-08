from flask import Flask, request, render_template, redirect, flash, jsonify, url_for
from flask_debugtoolbar import DebugToolbarExtension
from surveys import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.debug = True
debug = DebugToolbarExtension(app)

response = []
num_of_questions = len(questions)

@app.route('/')
def load_survey():
    # response.clear()
    return render_template('home.html', survey=satisfaction_survey, res_len=len(response))

@app.route('/question/<int:num>', methods=["GET", "POST"])
def question(num):
    if num != len(response) and len(response) < 4:
        return redirect(url_for('.question', num=len(response)))
    elif num != len(response) and len(response) == 4:
        return redirect('/thanks')
    print(response)
    return render_template('question.html', survey=satisfaction_survey, questions=questions, num=num, num_of_questions=num_of_questions)

@app.route('/answer/<int:num>')
def answer(num):
    choice = request.args.get('choice')
    if choice == None:
        flash('Please answer the question')
        return redirect(url_for('.question', num=num))
    else:
        new_num = num
        new_num += 1
        response.append(choice)
        print(response)
        return redirect(url_for('.question', num=new_num))

@app.route('/thanks')
def thank_you():
    choice = request.args.get('choice')
    if choice == None:
        flash('Please answer the question')
        return redirect(url_for('.question', num=len(response)))
    else:
        response.append(choice)
        print(response)
        if len(response) > 4:
            del response[-1]
        elif len(response) < 4:
            return redirect(url_for('.question', num=len(response)))
        else:
            return render_template('thanks.html')

