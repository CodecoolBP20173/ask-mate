import connection

QUESTION_FILE_NAME = 'sample_data/question.csv'
ANSWERS_FILE_NAME = 'sample_data/answer.csv'


@connection.connection_handler
def list_all_questions(cursor):
    cursor.execute("""SELECT * FROM question;""")
    all_questions = cursor.fetchall()
    return all_questions


@connection.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute("""SELECT * FROM question WHERE id = %(id)s;""", {'id': question_id})
    found_question = cursor.fetchall()
    return found_question


@connection.connection_handler
def get_answers_by_question_id(cursor, id):
    cursor.execute("""SELECT * FROM answer WHERE question_id = %(question_id)s;""", {'question_id': id})
    answers_for_question = cursor.fetchall()
    return answers_for_question


@connection.connection_handler
def add_new_question(cursor, new_data): # Needs testing
    '''new_data_list = [new_data['submission_time'], new_data['view_number'], new_data['vote_number'],
                     new_data['title'], new_data['message'], new_data['image']]'''
    cursor.execute("""INSERT INTO question(submission_time, view_number, vote_number, title, message, image) 
                      VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s);""", new_data)


@connection.connection_handler
def add_new_answer(cursor, new_data):
    pass


@connection.connection_handler
def update_question(data, filename, data_header):
    table = connection.get_data_from_file(filename)
    for row in table:
        row_number = table.index(row)
        if data['id'] == row['id']:
            table[row_number] = data
    return connection.write_data_to_file(table, data_header, filename)


@connection.connection_handler
def update_answer(data, filename, data_header):
    pass