# data structure:
# id: string
#     Unique and random generated (at least 2 special char()expect: ';'), 2 number, 2 lower and 2 upper case letter)
# name: string
# birth_date: number (year)

# importing everything you need
import os
from importlib.machinery import SourceFileLoader
current_file_path = os.path.dirname(os.path.abspath(__file__))
# User interface module
ui = SourceFileLoader("ui", current_file_path + "/../ui.py").load_module()
# data manager module
data_manager = SourceFileLoader("data_manager", current_file_path + "/../data_manager.py").load_module()
# common module
common = SourceFileLoader("common", current_file_path + "/../common.py").load_module()

# Constants
MIN_AGE = 16
MAX_AGE = 100
CURRENT_YEAR = 2017


# start this module by a module menu like the main menu
# user need to go back to the main menu from here
# we need to reach the default and the special functions of this module from the module menu
#
def start_module():
    file_name = current_file_path + "/persons.csv"
    table = data_manager.get_table_from_file(file_name)
    options = ["Show table",
               "Add a new item",
               "Remove by ID",
               "Update item by ID",
               "SPECIAL: Oldest persons",
               "SPECIAL: Persons closest to average age"]

    while True:
        ui.print_menu("Human Resources (HR) menu", options, "Back to main menu")
        try:
            inputs = ui.get_inputs(["Please enter a number: "], "")
            option = inputs[0]
            if option == "1":
                show_table(table)
            elif option == "2":
                table = add(table)
                if table is not None:
                    data_manager.write_table_to_file(file_name, table)
            elif option == "3":
                inputs = ui.get_inputs(["Please enter the person ID you want to delete: "], "")
                table = remove(table, inputs[0])
                if table is not None:
                    data_manager.write_table_to_file(file_name, table)
            elif option == "4":
                inputs = ui.get_inputs(["Please enter the person ID you want to update: "], "")
                table = update(table, inputs[0])
                if table is not None:
                    data_manager.write_table_to_file(file_name, table)
            elif option == "5":
                get_oldest_person(table)
            elif option == "6":
                get_persons_closest_to_average(table)
            elif option == "0":
                break
            else:
                raise KeyError("There is no such option.")
        except KeyError as err:
            ui.print_error_message(err)


# print the default table of records from the file
#
# @table: list of lists
def show_table(table):
    title_list = ["ID", "Name", "Birth year"]
    ui.print_table(table, title_list)


# Ask a new record as an input from the user than add it to @table, than return @table
#
# @table: list of lists
def add(table):
    title = "Add HR entry to table"
    entry_parameters = ["Please enter the name: ",
                        "Please enter the birth year: "]
    new_entry = ui.get_inputs(entry_parameters, title)
    if check_year_validity(MIN_AGE, MAX_AGE, new_entry[1]):
        row = [common.generate_random(table), new_entry[0], new_entry[1]]
        table.append(row)
    return table


# Remove the record having the id @id_ from the @list, than return @table
#
# @table: list of lists
# @id_: string
def remove(table, id_):
    return common.remove_by_id(table, id_)


# Update the record in @table having the id @id_ by asking the new data from the user,
# than return @table
#
# @table: list of lists
# @id_: string
def update(table, id_):
    line_to_update = common.search_by_id(table, id_)
    if line_to_update:
        title = "Update HR entry in table"
        entry_parameters = ["Enter updated Name, old value was {0}: ".format(table[line_to_update][1]),
                            "Enter updated birth year, old value was {0}: ".format(table[line_to_update][2])]
        new_entry = ui.get_inputs(entry_parameters, title)
        if check_year_validity(MIN_AGE, MAX_AGE, new_entry[1]):
            table[line_to_update][1] = new_entry[0]
            table[line_to_update][2] = new_entry[1]
    else:
        ui.print_error_message("Cannot update, entry not found!")
    return table


# special functions:
# ------------------

# the question: Who is the oldest person ?
# return type: list of strings (name or names if there are two more with the same value)
def get_oldest_person(table):
    result = list()
    oldest = 2147483647
    # Get the minimum year number
    for row in table:
        year = int(row[2])
        if oldest > year:
            oldest = year
    # Append all names to a new list whose year number matches oldest
    for row in table:
        if(int(row[2]) == oldest):
            result.append(row[1])
    ui.print_result(result, "The oldest person(s): ")
    return result


# the question: Who is the closest to the average age ?
# return type: list of strings (name or names if there are two more with the same value)
def get_persons_closest_to_average(table):
    result = list()
    average = 0.0
    for row in table:
        average += int(row[2])
    average = average / len(table)
    closest = 2147483647
    for row in table:
        current = abs(int(row[2]) - average)
        if closest > current:
            closest = current
    for row in table:
        year = int(row[2])
        if year >= average-closest and year <= average+closest:
            result.append(row[1])
    ui.print_result(result, "The person(s) closest to average: ")
    return result


def check_year_validity(MIN_AGE, MAX_AGE, year):
    year = int(year)
    if year:
        age = CURRENT_YEAR - year
        if age >= MIN_AGE:
            if age <= MAX_AGE:
                return True
            else:
                ui.print_error_message("Person is older than the maximum age, which is " + str(MAX_AGE))
                return False
        else:
            ui.print_error_message("Person is younger than the minimum age, which is " + str(MIN_AGE))
            return False
    else:
        ui.print_error_message("Not a number!")
        return False
