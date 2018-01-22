from flask import Blueprint, render_template, url_for
import data_manager
#from jinja2 import TemplatesNotFound

route_answer = Blueprint('answer', __name__, template_folder='templates')

@route_answer.route('/post_answer/' + '<question_id>')
def route_answer(question_id):
    return render_template('post_answer.html',
                           question_id=question_id,
                           question=data_manager.get_question_by_id(question_id),
                           req_url=url_for('route_display',
                                           question_id=question_id),
                           answers={})
