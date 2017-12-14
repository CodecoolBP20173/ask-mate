from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import data_manager
import connection

app = Flask(__name__)
URL_INDEX = '/'
URL_DISPLAY = '/display/'
URL_POST_ANSWER = '/post_answer/'
URL_ASK = '/ask'
UPLOAD_FOLDER = '/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route(URL_INDEX)
def route_index():
    return render_template(
        'index.html',
        questions=data_manager.list_all_questions())


@app.route(URL_ASK, methods=['GET', 'POST'])
def route_ask():
    if request.method == 'GET':
        return render_template('ask.html')
    else:
        question = {"id": str(data_manager.get_new_a_q_id(data_manager.QUESTION_FILE_NAME,
                                                          connection.DATA_HEADER_QUESTION)),
                    "submission_time": '',
                    "view_number": '0',
                    "vote_number": '0',
                    'title': request.form['title'],
                    'message': request.form['message'],
                    'image': ''}
        data_manager.add_new_a_q(question, data_manager.QUESTION_FILE_NAME, connection.DATA_HEADER_QUESTION)
        return redirect('/')


@app.route(URL_POST_ANSWER + '<question_id>')
def route_answer(question_id):
    return render_template('post_answer.html', question_id=question_id,
                           question=data_manager.get_question_by_id(question_id))


@app.route(URL_DISPLAY + '<question_id>', methods=['POST', 'GET'])
def route_display(question_id):
    if request.method == 'GET':
        return render_template(
            'display_question.html',
            question=data_manager.get_question_by_id(question_id),
            answers=data_manager.get_answers_by_question_id(question_id), question_id=question_id)
    else:  # method POST
        answer = {'id': str(data_manager.get_new_a_q_id(data_manager.ANSWERS_FILE_NAME,
                                                                    connection.DATA_HEADER_ANSWER)),
                  "submission_time": '',
                  'vote_number': '0',
                  'question_id': question_id,
                  'message': request.form['answer'],
                  'image': ''}
        data_manager.add_new_a_q(answer, data_manager.ANSWERS_FILE_NAME, connection.DATA_HEADER_ANSWER)
        return redirect(URL_DISPLAY + question_id)


@app.route('/display/<question_id>/<direction>', methods=['POST'])
def route_counter(question_id, direction):
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
    data_manager.update_q_and_a(updated_votes, data_manager.QUESTION_FILE_NAME, connection.DATA_HEADER_QUESTION)
    return redirect(URL_DISPLAY + question_id)


@app.route('/display/<question_id>/<response_id>/<direction>', methods=['POST'])
def route_counter_minus(question_id, response_id, direction):
    ans= data_manager.get_answers_by_question_id(question_id)
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
    data_manager.update_q_and_a(updated_votes, data_manager.ANSWERS_FILE_NAME, connection.DATA_HEADER_ANSWER)
    return redirect(URL_DISPLAY + question_id)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
