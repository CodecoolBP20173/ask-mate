from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import data_manager
import utility
import os
from datetime import datetime

app = Flask(__name__)
URL_INDEX = '/'
URL_DISPLAY = '/display/'
URL_POST_ANSWER = '/post_answer/'
URL_ASK = '/ask'
UPLOAD_FOLDER = "static/images"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route(URL_INDEX)
def route_index():
    questions = data_manager.list_all_questions_ordered_by_submission_time()
    return render_template(
        'index.html',
        questions=questions)


@app.route(URL_ASK, methods=['GET', 'POST'])
def route_ask():
    if request.method == 'GET':
        return render_template('ask.html', req_url=url_for('route_ask'), question={})
    else:
        file = request.files['file']
        if file and utility.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        question = {"submission_time": datetime.fromtimestamp(utility.display_unix_time()),
                    "view_number": 0,
                    "vote_number": 0,
                    'title': request.form['title'],
                    'message': request.form['message'],
                    'image': UPLOAD_FOLDER + '/' + filename if file.filename else ''}
        tempid = data_manager.add_new_question(question)

        return redirect(URL_DISPLAY + str(tempid))


@app.route(URL_POST_ANSWER + '<question_id>')
def route_answer(question_id):
    return render_template('post_answer.html', question_id=question_id,
                           question=data_manager.get_question_by_id(question_id),
                           req_url=url_for('route_display', question_id=question_id), answers={})


@app.route(URL_DISPLAY + '<question_id>', methods=['POST', 'GET'])
def route_display(question_id):
    if request.method == 'GET':
        answers = data_manager.get_answers_by_question_id(question_id)
        question = data_manager.get_question_by_id(question_id)
        return render_template(
            'display_question.html',
            question=question,
            answers=answers, question_id=question_id)
    else:
        answer = {'submission_time': datetime.today(),
                  'vote_number': 0,
                  'question_id': question_id,
                  'message': request.form['answer'],
                  'image': ''}
        print(answer)
        data_manager.add_new_answer(answer)
        return redirect(URL_DISPLAY + question_id)


@app.route('/display/<question_id>/<direction>', methods=['POST'])
def route_counter_question(question_id, direction):
    question = data_manager.get_question_by_id(question_id)
    if direction == 'up-vote':
        votes = int(question['vote_number'])
        votes += 1
    else:
        votes = int(question['vote_number'])
        votes -= 1
    updated_votes = {'id': question['id'],
                     "submission_time": question["submission_time"],
                     'view_number': question['view_number'],
                     'vote_number': votes,
                     'title': question['title'],
                     'message': question['message'],
                     'image': question['image']}
    data_manager.update_question(updated_votes)
    return redirect(URL_DISPLAY + question_id)


@app.route('/display/<question_id>/<response_id>/<direction>', methods=['POST'])
def route_counter_answer(question_id, response_id, direction):
    ans = data_manager.get_answers_by_question_id(question_id)
    for item in ans:
        if item['id'] == response_id:
            answers = item
    if direction == 'up-vote':
        votes = int(answers['vote_number'])
        votes += 1
    else:
        votes = int(answers['vote_number'])
        votes -= 1
    updated_votes = {'id': answers['id'],
                     "submission_time": answers["submission_time"],
                     'vote_number': votes,
                     'question_id': answers['question_id'],
                     'message': answers['message'],
                     'image': answers['image']}
    data_manager.update_answer(updated_votes)
    return redirect(URL_DISPLAY + question_id)


@app.route('/display/<question_id>/edit', methods=['GET', 'POST'])
def route_edit_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    if request.method == 'GET':
        return render_template('ask.html', question=question,
                               req_url=url_for('route_edit_question', question_id=question_id), question_id=question_id)
    else:
        updated_question = {'id': question['id'],
                            "submission_time": question["submission_time"],
                            'view_number': question['view_number'],
                            'vote_number': question['vote_number'],
                            'title': request.form['title'],
                            'message': request.form['message'],
                            'image': question['image']}
        data_manager.update_question(updated_question)
        return redirect(URL_DISPLAY + question_id)


@app.route('/display/<question_id>/<answer_id>/edit', methods=['GET', 'POST'])
def route_edit_answer(question_id, answer_id):
    if request.method == 'GET':
        answer = data_manager.get_answer_by_id(answer_id)
        question = data_manager.get_question_by_id(question_id)
        req_url = url_for('route_edit_answer', question_id=question_id, answer_id=answer_id)
        return render_template('post_answer.html', answers=answer, question=question, req_url=req_url)
    else:
        answer = data_manager.get_answer_by_id(answer_id)
        updated_votes = {'id': answer['id'],
                         "submission_time": answer["submission_time"],
                         'vote_number': answer['vote_number'],
                         'question_id': answer['question_id'],
                         'message': request.form['answer'],
                         'image': answer['image']}
        data_manager.update_answer(updated_votes)
        return redirect(URL_DISPLAY + question_id)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
