import connection

QUESTION_FILE_NAME = 'sample_data/question.csv'
ANSWERS_FILE_NAME = 'sample_data/answer.csv'


@connection.connection_handler
def list_all_questions_ordered_by_submission_time(cursor):
    cursor.execute("""
                      SELECT * FROM question
                      ORDER BY submission_time DESC;
                   """)
    all_questions = cursor.fetchall()
    return all_questions


@connection.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute("""SELECT * FROM question WHERE id = %(id)s;""", {'id': question_id})
    return cursor.fetchone()


@connection.connection_handler
def get_answers_by_question_id(cursor, id):
    cursor.execute("""SELECT * FROM answer WHERE question_id = %(question_id)s;""", {'question_id': id})
    answers_for_question = cursor.fetchall()
    return answers_for_question


@connection.connection_handler
def add_new_question(cursor, new_data): # Needs testing
    cursor.execute("""INSERT INTO question(submission_time, 
                                           view_number, 
                                           vote_number, 
                                           title, 
                                           message, 
                                           image) 
                      VALUES (%(submission_time)s, 
                              %(view_number)s,
                              %(vote_number)s, 
                              %(title)s, 
                              %(message)s, 
                              %(image)s);
                    """, new_data)

    cursor.execute("""SELECT id FROM question
                      ORDER BY id DESC
                      LIMIT 1;
                   """)

    return cursor.fetchone()['id']


@connection.connection_handler
def add_new_answer(cursor, new_data):
    cursor.execute("""INSERT INTO answer(submission_time, 
                                        vote_number, 
                                        question_id, 
                                        message, 
                                        image)
                      VALUES (%('submission_time')s, 
                              %('vote_number')s, 
                              %('question_id')s, 
                              %('message')s, 
                              %('image')s);
                    """, new_data)
    cursor.execute("""SELECT id FROM question
                      ORDER BY id DESC
                      LIMIT 1;
                    """)
    return cursor.fetchone('id')


@connection.connection_handler
def update_question(data, filename, data_header):
    @connection.connection_handler
    def update_question(cursor, data):
        cursor.execute("""
                        UPDATE question
                        SET submission_time = %{'submission_time'}s,
                        view_number = %{'view_number'}s,
                        vote_number = %{'vote_number'}s,
                        title = %{'title'}s,
                        message = %{'message'}s,
                        image = %{'image'}s
                        WHERE id = %{'id'}s;
                        """,
                       data)


@connection.connection_handler
def update_answer(cursor, new_data):
    cursor.execute("""
                      UPDATE answers
                      SET submission_time = %('submission_time')s, 
                      vote_number = %('vote_number')s, 
                      message = %('message')s, 
                      image = %('image')
                      WHERE id = %('id')s;
                  """, new_data)