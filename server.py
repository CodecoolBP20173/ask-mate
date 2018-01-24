from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import data_manager
import utility
import os
import user_handling
from datetime import datetime
from server_answer import route_answer_blueprint
from server_display import display
from server_search import route_search
from server_login_out import login

app = Flask(__name__)
app.register_blueprint(display, url_prefix="/display")
app.register_blueprint(route_answer_blueprint)
app.register_blueprint(route_search, url_prefix="/search")
app.register_blueprint(login, url_prefix="/login")
UPLOAD_FOLDER = "static/images"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def route_index():
    if 'user_id' in session:
        user_name = user_handling.get_user_name_by_id(session['user_id'])['user_name']
    else:
        user_name = None
    questions = data_manager.list_all_questions_ordered_by_submission_time()
    tags = utility.get_all_tags()
    return render_template(
        'index.html',
        questions=questions, tags=tags, user_name=user_name)


@app.route('/ask', methods=['GET', 'POST'])
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

        return redirect('/display/' + str(tempid))


@app.route('/question/<question_id>/new-tag', methods=['POST', 'GET'], defaults={'tag': None})
@app.route('/question/<question_id>/new-tag/<tag>')
def route_add_new_tag(question_id, tag):
    if request.method == 'GET' and tag is None:
        answers = data_manager.get_answers_by_question_id(question_id)
        question = data_manager.get_question_by_id(question_id)
        tags = utility.get_all_tags()
        question_tags = utility.get_tags_by_question_id(question_id)
        return render_template('new-tag.html',
                               answers=answers,
                               question=question,
                               question_id=question_id,
                               tags=tags,
                               question_tags=question_tags)
    else:
        new_question_tag = tag if tag else request.form["new-tag"]
        utility.add_tag_to_question(question_id, new_question_tag)
        return redirect(url_for('display.route_display', question_id=question_id))


@app.route('/question/<question_id>/new-comment', methods=['POST', 'GET'])
def route_add_new_comment(question_id):
    if request.method == 'GET':
        return render_template('post_answer.html',
                               question=data_manager.get_question_by_id(question_id),
                               answers={},
                               question_id=question_id,
                               req_url=url_for('route_add_new_comment',
                                               question_id=question_id))
    else:
        comment = {"submission_time": datetime.fromtimestamp(utility.display_unix_time()),
                   'message': request.form['answer'],
                   'question_id': question_id}
        utility.add_comment_to_question(comment)
        return redirect(url_for('display.route_display', question_id=question_id))


@app.route('/display/<question_id>/<response_id>/add-comment', methods=['POST', 'GET'])
def route_add_new_comment_answer(question_id, response_id):
    if request.method == 'GET':
        return render_template('post_answer.html',
                               question=data_manager.get_answer_by_id(response_id),
                               answers={},
                               question_id=question_id,
                               req_url=url_for('route_add_new_comment_answer',
                                               question_id=question_id,
                                               response_id=response_id))
    else:
        comment = {"submission_time": datetime.fromtimestamp(utility.display_unix_time()),
                   'message': request.form['answer'],
                   'answer_id': response_id}
        utility.add_comment_to_answer(comment)
        return redirect(url_for('display.route_display', question_id=question_id))


if __name__ == '__main__':
    app.secret_key = 'TheDoctorIsTheBest01'
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
