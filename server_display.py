from flask import Blueprint, render_template, request, redirect, url_for
import data_manager, utility
from datetime import datetime

display = Blueprint('display', __name__,
                        template_folder='templates')


@display.route('/<question_id>', methods=['POST', 'GET'])
def route_display(question_id):
    if request.method == 'GET':
        answers = data_manager.get_answers_by_question_id(question_id)
        question = data_manager.get_question_by_id(question_id)
        question_tags = utility.get_tags_by_question_id(question_id)
        question_comments = utility.show_comment_question(question_id)
        answer_comments = []
        for item in answers:
            sublist = utility.show_comment_answer(item['id'])
            for element in sublist:
                answer_comments.append(element)
        return render_template(
            'display_question.html',
            question=question,
            answers=answers,
            question_id=question_id,
            question_tags=question_tags,
            question_comments=question_comments,
            answer_comments=answer_comments)
    else:
        answer = {'submission_time': datetime.today(),
                  'vote_number': 0,
                  'question_id': question_id,
                  'message': request.form['answer'],
                  'image': ''}
        data_manager.add_new_answer(answer)
        return redirect('/display/' + question_id)


@display.route('/<question_id>/<direction>', methods=['POST'])
def route_counter_question(question_id, direction):
    question = data_manager.get_question_by_id(question_id)
    votes = int(question['vote_number'])
    votes += 1 if direction == 'up-vote' else -1
    updated_votes = {'id': question['id'],
                     "submission_time": question["submission_time"],
                     'view_number': question['view_number'],
                     'vote_number': votes,
                     'title': question['title'],
                     'message': question['message'],
                     'image': question['image']}
    data_manager.update_question(updated_votes)
    return redirect('/display/' + question_id)


@display.route('/<question_id>/<response_id>/<direction>', methods=['POST'])
def route_counter_answer(question_id, response_id, direction):
    answers = data_manager.get_answer_by_id(response_id)
    votes = int(answers['vote_number'])
    votes += 1 if direction == 'up-vote' else -1
    updated_votes = {'id': answers['id'],
                     "submission_time": answers["submission_time"],
                     'vote_number': votes,
                     'question_id': answers['question_id'],
                     'message': answers['message'],
                     'image': answers['image']}
    data_manager.update_answer(updated_votes)
    return redirect('/display/' + question_id)


@display.route('/<question_id>/edit', methods=['GET', 'POST'])
def route_edit_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    if request.method == 'GET':
        return render_template('ask.html', question=question,
                               req_url=url_for('display.route_edit_question',
                                               question_id=question_id),
                               question_id=question_id)
    else:
        updated_question = {'id': question['id'],
                            "submission_time": question["submission_time"],
                            'view_number': question['view_number'],
                            'vote_number': question['vote_number'],
                            'title': request.form['title'],
                            'message': request.form['message'],
                            'image': question['image']}
        data_manager.update_question(updated_question)
        return redirect('/display/' + question_id)


@display.route('/<question_id>/<answer_id>/edit', methods=['GET', 'POST'])
def route_edit_answer(question_id, answer_id):
    if request.method == 'GET':
        answer = data_manager.get_answer_by_id(answer_id)
        question = data_manager.get_question_by_id(question_id)
        req_url = url_for('display.route_edit_answer',
                          question_id=question_id,
                          answer_id=answer_id)
        return render_template('post_answer.html',
                               answers=answer,
                               question=question,
                               req_url=req_url)
    else:
        answer = data_manager.get_answer_by_id(answer_id)
        updated_votes = {'id': answer['id'],
                         "submission_time": answer["submission_time"],
                         'vote_number': answer['vote_number'],
                         'question_id': answer['question_id'],
                         'message': request.form['answer'],
                         'image': answer['image']}
        data_manager.update_answer(updated_votes)
        return redirect('/display/' + question_id)


@display.route('/<question_id>/delete', methods=['GET', 'POST'])
def route_delete_question(question_id):
    utility.delete_question_and_answers(question_id)
    return redirect('')


@display.route('/<question_id>/<answer_id>/delete', methods=['GET', 'POST'])
def route_delete_answer(question_id, answer_id):
    utility.delete_answer(answer_id)
    return redirect('/display/' + question_id)