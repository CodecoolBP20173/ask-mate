from flask import Blueprint, render_template, request
import data_manager

route_search = Blueprint('search', __name__, template_folder='templates')


@route_search.route('/questions', methods=['POST'])
def route_search_question():
    pattern = request.form["search_input"]
    questions = data_manager.search_questions(pattern)
    return render_template('index.html', questions=questions)


@route_search.route('/answer/<question_id>', methods=['POST'])
def route_search_answer(question_id):
    pattern = request.form["search_input"]
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.search_answer(pattern)
    return render_template('display_question.html',
                           question=question,
                           answers=answers,
                           question_id=question_id)

