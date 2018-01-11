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
def get_answer_by_id(cursor, answer_id):
    cursor.execute("""SELECT * FROM answer
                      WHERE id = %(id)s
                      ORDER BY submission_time;""", {'id': answer_id})
    return cursor.fetchone()


@connection.connection_handler
def get_answers_by_question_id(cursor, id):
    cursor.execute("""SELECT * FROM answer
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
    print(new_data)
    cursor.execute("""INSERT INTO answer(submission_time, 
                                        vote_number, 
                                        question_id, 
                                        message, 
                                        image)
                      VALUES (%(submission_time)s, 
                              %(vote_number)s, 
                              %(question_id)s, 
                              %(message)s, 
                              %(image)s);
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
                    SELECT * FROM question
                    INNER JOIN answer ON question.id = answer.question_id
                    WHERE title LIKE %(pattern)s
                    OR
                    question.message LIKE %(pattern)s
                    OR
                    answer.message LIKE %(pattern)s
                    ORDER BY question.id DESC;
                    """,
                   {'pattern': '%' + pattern + '%'})
    return cursor.fetchall()


@connection.connection_handler
def search_answer(cursor, pattern):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE message LIKE %(pattern)s
                    ORDER BY id DESC;
                    """,
                   {'pattern': '%' + pattern + '%'})
    return cursor.fetchall()


@connection.connection_handler
def get_all_tags(cursor):
    cursor.execute("""
                    SELECT * FROM tag;
                    """)
    return cursor.fetchall()


@connection.connection_handler
def get_tags_by_question_id(cursor, question_id):
    cursor.execute("""SELECT name FROM tag 
                      INNER JOIN question_tag ON question_tag.tag_id=tag.id 
                      WHERE question_id=%(q_id)s;""",
                   {'q_id': question_id})
    return cursor.fetchall()


@connection.connection_handler
def add_new_tag(cursor, tag_name):
    cursor.execute("""INSERT INTO tag (name) 
                      VALUES (%(name)s);""",
                   {'name': tag_name})
    cursor.execute("""SELECT id FROM tag
                      WHERE name = %(t_name)s;""",
                   {'t_name': tag_name})
    result = cursor.fetchone()
    return result


@connection.connection_handler
def create_question_tag_relation(cursor, question_id, tag_id):
    cursor.execute("""
                    SELECT * FROM question_tag
                    WHERE question_id=%(qid)s
                    AND
                    tag_id=%(tid)s;
                    """, {'qid': question_id, 'tid': tag_id})
    if not cursor.fetchone():
        cursor.execute("""INSERT INTO question_tag (question_id, tag_id)
                          VALUES (%(q_id)s, %(t_id)s);""",
                       {'q_id': question_id, 't_id': tag_id})


@connection.connection_handler
def add_tag_to_question(cursor, question_id, tag_name):
    cursor.execute("""SELECT id FROM tag
                      WHERE name = %(t_name)s;""",
                   {'t_name': tag_name})
    result = cursor.fetchone()
    if result:
        create_question_tag_relation(question_id, result['id'])
    else:
        tag_id = add_new_tag(tag_name)['id']
        create_question_tag_relation(question_id, tag_id)


@connection.connection_handler
def delete_answer(cursor, answer_id):
    deactivate_answer_comments(answer_id)
    cursor.execute("""
                    DELETE FROM answer
                    WHERE id = %(answer_id)s;
                  """, {'answer_id': answer_id})


@connection.connection_handler
def delete_question_and_answers(cursor, question_id):
    deactivate_question_comments(question_id)
    cursor.execute("""
                    DELETE FROM answer
                    WHERE question_id=%(qid)s;
                    """, {'qid': question_id})
    cursor.execute("""
                    DELETE FROM question_tag
                    WHERE question_id=%(question_id)s;
                    """, {'question_id': question_id})
    cursor.execute("""
                    DELETE FROM question
                    WHERE id=%(qid)s;
                    """, {'qid': question_id})


@connection.connection_handler
def deactivate_answer_comments(cursor, answer_id):
    cursor.execute("""
                    UPDATE comment
                    SET answer_id=NULL
                    WHERE answer_id=%(answer_id)s;
                    """, {'answer_id': answer_id})


@connection.connection_handler
def deactivate_question_comments(cursor, question_id):
    cursor.execute("""
                    UPDATE comment
                    SET question_id=NULL
                    WHERE question_id=%(question_id)s;
                    """, {'question_id': question_id})
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE question_id=%(question_id)s;
                    """, {'question_id': question_id})
    results=cursor.fetchall()
    for answer in results:
        deactivate_answer_comments(answer['id'])


@connection.connection_handler
def show_comment_question(cursor, question_id):
    cursor.execute("""SELECT message FROM comment WHERE question_id = %(q_id)s;""",
                   {'q_id': question_id})
    comments = cursor.fetchall()
    return comments


@connection.connection_handler
def add_comment_to_question(cursor, new_comment):
    cursor.execute("""INSERT INTO comment(question_id, message, submission_time) VALUES 
                      (%(question_id)s, %(message)s, %(submission_time)s);""", new_comment)


@connection.connection_handler
def show_comment_answer(cursor, answer_id):
    cursor.execute("""SELECT * FROM comment WHERE answer_id = %(a_id)s;""",
                   {'a_id': answer_id})
    comments = cursor.fetchall()
    return comments


@connection.connection_handler
def add_comment_to_answer(cursor, new_comment):
    cursor.execute("""INSERT INTO comment(answer_id, message, submission_time) VALUES 
                      (%(answer_id)s, %(message)s, %(submission_time)s);""", new_comment)
