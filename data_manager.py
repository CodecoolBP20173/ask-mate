import connection

QUESTION_FILE_NAME = 'sample_data/question.csv'
ANSWERS_FILE_NAME = 'sample_data/answer.csv'


@connection.connection_handler
def list_all_questions_ordered_by_submission_time(cursor):
    cursor.execute("""
                      SELECT q.id, q.title, q.submission_time, q.image, q.message, q.view_number,
                      q.vote_number, q.user_id, COALESCE(u.user_name, 'Anonymous') AS user_name
                      FROM question AS q
                      LEFT JOIN users AS u
                      ON q.user_id=u.id
                      ORDER BY submission_time DESC;
                   """)
    all_questions = cursor.fetchall()
    return all_questions


@connection.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute("""SELECT q.id, q.title, q.submission_time, q.image, q.message, q.view_number,
                      q.vote_number, q.user_id, COALESCE(u.user_name, 'Anonymous') AS user_name
                      FROM question AS q
                      LEFT JOIN users AS u
                      ON q.user_id=u.id
                      WHERE q.id =%(id)s;""", {'id': question_id})
    return cursor.fetchone()


@connection.connection_handler
def get_questions_by_tag(cursor, tag):
    """
    :param tag:
    :return: List of dictionaries, where every dictionary contains a questions, with
    the following keys: id, submission_time, title, view_number, vote_number
    """
    cursor.execute("""
                   SELECT DISTINCT question.id, question.submission_time, 
                          question.view_number, question.vote_number, question.title
                    FROM question
                    LEFT JOIN question_tag ON question.id = question_tag.question_id
                    LEFT JOIN tag ON tag.id = question_tag.tag_id
                    WHERE tag.name = %(tag)s;
                   """, {'tag': tag})
    return cursor.fetchall()


@connection.connection_handler
def get_answer_by_id(cursor, answer_id):
    cursor.execute("""SELECT * FROM answer
                      WHERE id = %(id)s;""", {'id': answer_id})
    return cursor.fetchone()


@connection.connection_handler
def get_answers_by_question_id(cursor, id):
    cursor.execute("""SELECT a.id, a.submission_time, a.vote_number, a.question_id, a.message, a.image,
                      COALESCE(u.user_name, 'Anonymous') AS user_name FROM answer AS a 
                      LEFT JOIN users AS u 
                      ON a.user_id = u.id
                      WHERE question_id = %(question_id)s
                      ORDER BY submission_time;""", {'question_id': id})
    answers_for_question = cursor.fetchall()
    return answers_for_question


@connection.connection_handler
def add_new_question(cursor, new_data):
    cursor.execute("""INSERT INTO question(submission_time, 
                                           view_number, 
                                           vote_number, 
                                           title, 
                                           message, 
                                           image,
                                           user_id) 
                      VALUES (%(submission_time)s, 
                              %(view_number)s,
                              %(vote_number)s, 
                              %(title)s, 
                              %(message)s, 
                              %(image)s,
                              %(user_id)s);
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
                                        image,
                                        user_id)
                      VALUES (%(submission_time)s, 
                              %(vote_number)s, 
                              %(question_id)s, 
                              %(message)s, 
                              %(image)s,
                              %(user_id)s);
                    """, new_data)


@connection.connection_handler
def update_question(cursor, data):
    cursor.execute("""
                    UPDATE question
                    SET submission_time = %(submission_time)s,
                    view_number = %(view_number)s,
                    vote_number = %(vote_number)s,
                    title = %(title)s,
                    message = %(message)s,
                    image = %(image)s
                    WHERE id = %(id)s;
                    """,
                   data)


@connection.connection_handler
def update_answer(cursor, new_data):
    cursor.execute("""
                      UPDATE answer
                      SET submission_time = %(submission_time)s, 
                      vote_number = %(vote_number)s, 
                      message = %(message)s, 
                      image = %(image)s
                      WHERE id = %(id)s;
                  """, new_data)


@connection.connection_handler
def search_questions(cursor, pattern):
    cursor.execute("""
                    SELECT DISTINCT question.vote_number, question.message, question.view_number,
                    question.title, question.submission_time, question.id, question.image
                    FROM question
                    LEFT JOIN answer ON question.id = answer.question_id
                    WHERE LOWER(question.title) LIKE %(pattern)s
                    OR
                    LOWER(question.message) LIKE %(pattern)s
                    OR
                    LOWER(answer.message) LIKE %(pattern)s
                    ORDER BY question.submission_time DESC;
                    """,
                   {'pattern': '%' + pattern.lower() + '%'})
    return cursor.fetchall()


@connection.connection_handler
def search_answer(cursor, pattern):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE LOWER(message) LIKE %(pattern)s
                    ORDER BY id DESC;
                    """,
                   {'pattern': '%' + pattern.lower() + '%'})
    return cursor.fetchall()


@connection.connection_handler
def delete_comment(cursor, comment_id):
    cursor.execute("""DELETE FROM comment WHERE id = %(cid)s;""", {'cid': comment_id})