# implement commonly used functions here
import random
import string
import time
import os
from importlib.machinery import SourceFileLoader
current_file_path = os.path.dirname(os.path.abspath(__file__))
# User interface module
ui = SourceFileLoader("ui", current_file_path + "/ui.py").load_module()
# data manager module
data_manager = SourceFileLoader("data_manager", current_file_path + "/data_manager.py").load_module()


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


# find the given data from different databases
# input: database, data to search
# output: list of found data, ID, name
# May need modification for Daily Menu option
def search(database, data):
    ID = 0
    FOOD = 1
    WEIGHT = 2
    MEASURE = 3
    PHE_PER_MEAS = 4

    result = []
    for row in database:
        if data in row:
            recent_row = row.split(",")
            result.append([recent_row[FOOD], recent_row[WEIGHT], recent_row[PHE_PER_MEAS]])
    return result


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


def handle_database_menu():
    database_search = ui.get_inputs(["Please enter a food name: "], "Search in database")
    usa_database = data_manager.import_csv_file()
    search_results = search(usa_database, database_search)
    menu_list = []
    for i in search_results:
        menu_list.append(i[0])
    ui.print_menu("Search results:", menu_list, "Return to menu")
    inputs = ui.get_inputs(["Please enter a number: "], "")
    chosen_food = search_results[int(inputs[0]) - 1]
    returned_phe_content = database_based_phe_calculation(chosen_food)
    return (chosen_food, returned_phe_content)


def database_based_phe_calculation(food_data,):
    input_weight = float(ui.get_inputs(["Please enter the weight in grams: "], ""))
    phe_content = ((input_weight * float(food_data[2][2:-2])) / float(food_data[1][2:-1])) * 1000
    return phe_content

