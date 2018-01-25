import bcrypt
import connection
from functools import wraps
from flask import session, redirect, url_for
import data_manager


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@connection.connection_handler
def new_user_to_db(cursor, new_user_information):
    cursor.execute("""INSERT INTO users(
                                        user_name, 
                                        registration_date, 
                                        password,
                                        email) 
                      VALUES (%(user_name)s, 
                              %(registration_date)s, 
                              %(password)s,
                              %(email)s);""", new_user_information)


@connection.connection_handler
def get_password_hash_from_db(cursor, username):
    cursor.execute("""SELECT password, id FROM users WHERE user_name=%(user_name)s""",
                   {'user_name': username})
    return cursor.fetchone()


@connection.connection_handler
def get_user_name_by_id(cursor, user_id):
    cursor.execute("""
                    SELECT user_name, registration_date, COALESCE(email, 'No email address') AS email FROM users
                    WHERE id=%(user_id)s;
                    """, {'user_id': user_id})
    return cursor.fetchone()


@connection.connection_handler
def get_user_list(cursor):
    cursor.execute("""
                    SELECT id, user_name, registration_date, COALESCE(email, 'No email address') AS email
                    FROM users ORDER BY user_name;
                    """)
    return cursor.fetchall()


@connection.connection_handler
def get_user_questions_by_id(cursor, user_id):
    cursor.execute("""SELECT * FROM question WHERE user_id=%(user_id)s;""", {'user_id': user_id})
    return cursor.fetchall()


@connection.connection_handler
def get_user_comments_by_id(cursor, user_id):
    cursor.execute("""SELECT * FROM comment WHERE user_id=%(user_id)s;""", {'user_id': user_id})
    return cursor.fetchall()


@connection.connection_handler
def get_user_answers_by_id(cursor, user_id):
    cursor.execute("""SELECT * FROM answer WHERE user_id=%(user_id)s;""", {'user_id': user_id})
    return cursor.fetchall()


def login_required(function):
    @wraps(function)
    def wrap(*args, **kwargs):
        if 'user_id' in session:
            return function(*args, **kwargs)
        else:
            return redirect(url_for('login.login_check')+"login_error")
    return wrap


@connection.connection_handler
def delete_comment_by_answer(cursor, answer_id):
    cursor.execute("""DELETE FROM comment 
                      WHERE answer_id=%(answer_id)s;""",
                   {'answer_id': answer_id})


@connection.connection_handler
def delete_comment_by_question(cursor, question_id):
    cursor.execute("""DELETE FROM comment 
                      WHERE question_id=%(question_id)s;""",
                   {'question_id': question_id})


@connection.connection_handler
def delete_answer_comment_by_question_id(cursor, question_id):
    answers = data_manager.get_answers_by_question_id(question_id)
    for answer in answers:
        delete_comment_by_answer(answer['id'])
