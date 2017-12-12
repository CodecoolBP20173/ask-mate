from flask import Flask, render_template, request, redirect

import data_manager

app = Flask(__name__)
URL_INDEX = '/'
URL_DISPLAY = '/display/'


@app.route(URL_INDEX)
def route_index():
    return render_template('index.html', questions=data_manager.list_all_questions())


@app.route(URL_DISPLAY, methods=['POST', 'GET'])
@app.route(URL_DISPLAY + '<question_id>', methods=['POST', 'GET'])
def route_display(question_id):
    if request.method == 'GET':
        return render_template('display_question.html', question=data_manager.get_question_by_id(question_id),
                               answers=data_manager.get_answers_by_question_id(question_id))
    else:
        if request.method == 'POST':
            answer = {'id': '',
                      "submission_time":'',
                      'vote_number':'',
                      'question_id': question_id,
                      'message':'',
                      'image':''}



if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )