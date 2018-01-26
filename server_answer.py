from flask import Blueprint, render_template, url_for
import data_manager
from server_display import display
import user_handling

route_answer_blueprint = Blueprint('answer', __name__, template_folder='templates')

@route_answer_blueprint.route('/post_answer/' + '<question_id>')
@user_handling.login_required
def route_answer(question_id):
    return render_template('post_answer.html',
                           question_id=question_id,
                           question=data_manager.get_question_by_id(question_id),
                           req_url=url_for('display.route_display',
                                           question_id=question_id),
                           answers={})
