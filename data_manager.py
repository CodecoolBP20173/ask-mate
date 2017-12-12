import connection

QUESTION_FILE_NAME = '/sample_data/question.csv'
ANSWERS_FILE_NAME = '/sample_data/answer.csv'

def list_all_questions():
    return connection.get_data_from_file(QUESTION_FILE_NAME)


def get_question_by_id(id):
    pass


def get_answers_by_question_id(id):
    pass