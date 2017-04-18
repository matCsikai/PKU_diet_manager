# data structure:
# id: string
#     Unique and random generated (at least 2 special char()expect: ';'), 2 number, 2 lower and 2 upper case letter)
# name: stringe
# manufacturer: string
# purchase_date: number (year)
# durability: number (year)


# importing everything you need
import os
import datetime
from importlib.machinery import SourceFileLoader
current_file_path = os.path.dirname(os.path.abspath(__file__))
# User interface module
ui = SourceFileLoader("ui", current_file_path + "/../ui.py").load_module()
# data manager module
data_manager = SourceFileLoader("data_manager", current_file_path + "/../data_manager.py").load_module()
# common module
common = SourceFileLoader("common", current_file_path + "/../common.py").load_module()

# Constants
CURRENT_YEAR = 2017


# start this module by a module menu like the main menu
# user need to go back to the main menu from here
# we need to reach the default and the special functions of this module from the module menu
#
def start_module():
    file_name = current_file_path + "/tools.csv"
    table = data_manager.get_table_from_file(file_name)
    options = ["Show table",
               "Add a new item",
               "Remove item by ID",
               "Update item by ID",
               "SPECIAL: Items that haven't exceeded their durability",
               "SPECIAL: Average durability per manufacturer"]

    while True:
        try:
            ui.print_menu("Tool manager Menu", options, "Back to main menu")
            inputs = ui.get_inputs(["Please enter a number: "], "")
            option = inputs[0]
            file_name = "tools.csv"
            if option == "1":
                show_table(table)
            elif option == "2":
                table = add(table)
                if table is not None:
                    data_manager.write_table_to_file(file_name, table)
            elif option == "3":
                inputs = ui.get_inputs(["Please enter the tool ID you want to delete: "], "")
                table = remove(table, inputs[0])
                if table is not None:
                    data_manager.write_table_to_file(file_name, table)
            elif option == "4":
                inputs = ui.get_inputs(["Please enter the tool ID you want to update: "], "")
                table = update(table, inputs[0])
                if table is not None:
                    data_manager.write_table_to_file(file_name, table)
            elif option == "5":
                get_available_tools(table)
            elif option == "6":
                get_average_durability_by_manufacturers(table)
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
    title_list = ["ID", "Name", "Manufacturer", "Purchase date", "Durability"]
    ui.print_table(table, title_list)


# Ask a new record as an input from the user than add it to @table, than return @table
#
# @table: list of lists
def add(table):
    NAME_INDEX = 0
    MANUFACTURER_INDEX = 1
    PURCHASE_DATE_INDEX = 2
    DURABILITY_INDEX = 3
    validity_checklist = [False, False]
    validated_entry = [common.generate_random(table)]
    title = "Add tool entry to table"
    entry_parameters = ["Please enter the name of tool: ",
                        "Please enter manufacturer: ",
                        "Please enter purchase date: ",
                        "Please enter the durability: "]
    while False in validity_checklist:  # Loop asking for input, until input passes every test.
        new_entry = ui.get_inputs(entry_parameters, title)

        # Check if the purchase year is correct: whether it is int, then whether it is less or equal to current year.
        try:
            int(new_entry[PURCHASE_DATE_INDEX])
        except ValueError as err:
            ui.print_error_message(err)
        else:
            if int(new_entry[PURCHASE_DATE_INDEX]) <= datetime.date.today().year:
                validity_checklist[0] = True
            elif int(new_entry[PURCHASE_DATE_INDEX]) > datetime.date.today().year:
                ui.print_error_message("Incorrect date (year)")

        # Check if durability entry is integer
        try:
            int(new_entry[DURABILITY_INDEX])
        except ValueError as err:
            ui.print_error_message(err)
        else:
            validity_checklist[1] = True

    for data_field in new_entry:
        validated_entry.append(str(data_field))

    table.append(validated_entry)
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
    ID_INDEX = 0
    NAME_INDEX = 1
    MANUFACTURER_INDEX = 2
    PURCHASE_DATE_INDEX = 3
    DURABILITY_INDEX = 4

    line_to_update_index = None
    for index, line in enumerate(table):
        if line[ID_INDEX] == id_:
            line_to_update_index = index
            break

    if line_to_update_index is None:
        ui.print_error_message("No such ID exists in table.")
        return table

    validity_checklist = [False, False]
    title = "Update tool manager entry"
    entry_parameters = ["Enter updated name, old value was {0}: ".format(table[line_to_update_index][NAME_INDEX]),
                        "Enter updated manufacturer, old value was {0}: ".format(table[line_to_update_index][MANUFACTURER_INDEX]),
                        "Enter updated purchase year, old value was {0}: ".format(table[line_to_update_index][PURCHASE_DATE_INDEX]),
                        "Enter updated durability, old value was {0}: ".format(table[line_to_update_index][DURABILITY_INDEX])]

    while False in validity_checklist:  # Loop asking for input, until input passes every test.
        new_entry = [id_]
        new_entry.extend(ui.get_inputs(entry_parameters, title))

        # Check if the purchase year is correct: whether it is int, then whether it is less or equal to current year.
        try:
            int(new_entry[PURCHASE_DATE_INDEX])
        except ValueError as err:
            ui.print_error_message(err)
        else:
            if int(new_entry[PURCHASE_DATE_INDEX]) <= datetime.date.today().year:
                validity_checklist[0] = True
            elif int(new_entry[PURCHASE_DATE_INDEX]) > datetime.date.today().year:
                ui.print_error_message("Incorrect date (year)")

        # Check if durability entry is integer
        try:
            int(new_entry[DURABILITY_INDEX])
        except ValueError as err:
            ui.print_error_message(err)
        else:
            validity_checklist[1] = True

    for index in range(1, len(table[line_to_update_index])):
        table[line_to_update_index][index] = str(new_entry[index])

    return table


# special functions:
# ------------------

# the question: Which items has not yet exceeded their durability ?
# return type: list of lists (the inner list contains the whole row with their actual data types)
#
# @table: list of lists
def get_available_tools(table):
    result = list()
    for row in table:
        row[3] = int(row[3])
        row[4] = int(row[4])
        if row[3] + row[4] > CURRENT_YEAR:
            result.append(row)
    return result

# the question: What are the average durability time for each manufacturer?
# return type: a dictionary with this structure: { [manufacturer] : [avg] }
#
# @table: list of lists
def get_average_durability_by_manufacturers(table):
    avg_durability = dict()
    for row in table:
        if row[2] not in avg_durability:
            avg_durability[row[2]] = [int(row[4]), 1]
        else:
            avg_durability[row[2]][0] += int(row[4])
            avg_durability[row[2]][1] += 1
    result = dict()
    for key, value in avg_durability.items():
        result[key] = value[0] / value[1]
    return result
