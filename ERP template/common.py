# implement commonly used functions here
import random
import string
import time
import os
from importlib.machinery import SourceFileLoader
current_file_path = os.path.dirname(os.path.abspath(__file__))

# User interface module
ui = SourceFileLoader("ui", current_file_path + "/ui.py").load_module()


# generate and return a unique and random string
# other expectation:
# - at least 2 special char()expect: ';'), 2 number, 2 lower and 2 upper case letter
# - it must be unique in the list
#
# @table: list of list
# @generated: string - generated random string (unique in the @table)
def generate_random(table):
    UNIQUE_ID_LENGTH = 8
    ID_INDEX = 0
    random.seed(a=int(time.time()), version=2)
    generated_not_in_list = False

    while not generated_not_in_list:
        char = []
        for _ in range(2):
            char.append(random.choice(string.ascii_lowercase))
            char.append(random.choice(string.ascii_uppercase))
            char.append(random.choice(string.digits))

        while len(char) < UNIQUE_ID_LENGTH:
            special_character = random.choice(string.punctuation)
            if special_character != ";":
                char.append(special_character)
            else:
                continue

        random.shuffle(char)
        generated = ''.join(char)
        generated_not_in_list = True
        for line in table:
            if line[ID_INDEX] == generated:
                generated_not_in_list = False
    return generated


def remove_by_id(table, id_):
    line_to_remove = [i for i, j in enumerate(table) if id_ in j]
    if not line_to_remove:
        ui.print_error_message("There is no such ID in the table.")
    else:
        table.pop(int(line_to_remove[0]))
        return table


def is_int(number):
    try:
        a = int(number)
        return True
    except:
        return False


def search_by_id(table, id_):
    row_to_remove = [i for i, j in enumerate(table) if id_ in j]
    if not row_to_remove:
        ui.print_error_message("There is no such ID in the table.")
    return row_to_remove[0]


def check_date_for_validity(year, month, day):

    day = int(day)
    month = int(month)
    year = int(year)
    error_msg = ""

    MONTHS_W_30 = [3, 6, 9, 11]
    MONTHS_W_31 = [1, 3, 5, 7, 8, 10, 12]
    FEBRUARY = 2
    CURRENT_YEAR = 2017

    if year > CURRENT_YEAR:
        error_msg += "Year cannot be higher than the current one!\n"
    if month < 1 or month > 12:
        error_msg += "Month has to be an integer between 1 and 12"
    if month in MONTHS_W_30:
        if day < 1 or day > 30:
            error_msg += "With the chosen month, day must be within 1 and 30"
    elif month in MONTHS_W_31:
        if day < 1 or day > 31:
                error_msg += "With the chosen month, day must be within 1 and 31"
    elif month == FEBRUARY and year % 4 == 0:
        if day < 1 or day > 29:
            error_msg += "With February chosen as month in leap year, day must be between 1 and 29"
    elif month == FEBRUARY and year % 4 != 0:
        if day < 1 or day > 28:
            error_msg += "With February chosen as month in non leap year, day must be between 1 and 28"

    if len(error_msg) != 0:
        raise ValueError(error_msg)