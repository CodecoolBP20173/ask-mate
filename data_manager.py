import connection

QUESTION_FILE_NAME = 'sample_data/question.csv'
ANSWERS_FILE_NAME = 'sample_data/answer.csv'


def list_all_questions():
    return connection.get_data_from_file(QUESTION_FILE_NAME)


def get_question_by_id(question_id):
    table = list_all_questions()
    string_id = str(question_id)
    for question_dict in table:
        if question_dict['id'] == string_id:
            return question_dict


def get_answers_by_question_id(id):
    table = connection.get_data_from_file(ANSWERS_FILE_NAME)
    answers_for_question = []
    for answer_dict in table:
        if answer_dict['question_id'] == id:
            answers_for_question.append(answer_dict)
    return answers_for_question


def get_new_a_q_id(filename, data_header):
    max_id = 0
    data = connection.get_data_from_file(filename)
    for num in range(1, len(data)):
        act_id = int(data[num][data_header[0]])
        if act_id > max_id:
            max_id = act_id
    return max_id + 1


def add_new_a_q(data, filename, data_header):
    all_answers = connection.get_data_from_file(filename)
    all_answers.append(data)
    connection.write_data_to_file(all_answers, data_header, filename)


def update_q_and_a(data, filename, data_header):
    table = connection.get_data_from_file(filename)
    for row in table:
        row_number = table.index(row)
        if data['id'] == row['id']:
            table[row_number] = data
    return connection.write_data_to_file(table, data_header, filename)

