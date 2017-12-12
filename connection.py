import csv

DATA_HEADER_ANSWER = ["id", "submisson_time", "vote_number", "question_id", "message", "image"]
DATA_HEADER_QUESTION = ["id", "submisson_time", "view_number", "vote_number", "title", "message", "image"]


def get_data_from_file(filename):
    """ Reads a .csv file and returns a list of dictionaries
    with respect of line breaks and colons in the file """

    with open(filename, "r", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        questions = []
        for row in reader:
            question = dict(row)
            questions.append(question)
        return questions


def write_data_to_file(list_to_write, data_header, filename):
    """ Writes all data (list of dictionary) into a .csv file.
    Returns: None """

    with open(filename, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data_header)
        writer.writeheader()
        for row in list_to_write:
            writer.writerow(row)
