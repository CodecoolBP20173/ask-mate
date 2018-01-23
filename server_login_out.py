from flask import Blueprint, render_template, request, redirect, url_for, session
import data_manager, utility, user_handling
from datetime import datetime

login = Blueprint('login', __name__, template_folder='templates')


@login.route('/register', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        questions = data_manager.list_all_questions_ordered_by_submission_time()
        return render_template('registration.html')
    else:
        new_user_data={'user_name': request.form['user_name'],
                       'password': user_handling.hash_password(request.form['password']),
                       'registration_date': datetime.fromtimestamp(utility.display_unix_time())}
        user_handling.new_user_to_db(new_user_data)
        return redirect('/')


@login.route('/', methods=['GET','POST'])
def login_check():
    if request.method == 'GET':
        questions = data_manager.list_all_questions_ordered_by_submission_time()
        return render_template('register_login.html', questions=questions)
    else:
        hash = user_handling.get_password_hash_from_db(request.form['user_name'])
        user_handling.verify_password(request.form['password'], hash['password'])
        session['user_id'] = hash['id']
        return redirect('/')