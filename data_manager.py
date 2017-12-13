import connection

QUESTION_FILE_NAME = 'sample_data/question.csv'
ANSWERS_FILE_NAME = 'sample_data/answer.csv'


def list_all_questions():
    return connection.get_data_from_file(QUESTION_FILE_NAME)


def get_question_by_id(question_id):
    table = list_all_questions()
    for question_dict in table:
        if question_dict['id'] == question_id:
            return question_dict


def get_answers_by_question_id(id):
    table = connection.get_data_from_file(ANSWERS_FILE_NAME)
    answers_for_question = []
    for answer_dict in table:
        if answer_dict['question_id'] == id:
            answers_for_question.append(answer_dict)
    return answers_for_question


def get_new_answer_id():
    max_id = 0
    data = connection.get_data_from_file(ANSWERS_FILE_NAME)
    for num in range(1, len(data)):
        act_id = int(data[num][connection.DATA_HEADER_ANSWER[0]])
        if act_id > max_id:
            max_id = act_id
    return max_id + 1


def add_new_answer(answer):
    all_answers = connection.get_data_from_file(ANSWERS_FILE_NAME)
    all_answers.append(answer)
    connection.write_data_to_file(all_answers, connection.DATA_HEADER_ANSWER, ANSWERS_FILE_NAME)