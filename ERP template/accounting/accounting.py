# data structure:
# id: string
#     Unique and random generated (at least 2 special char()expect: ';'), 2 number, 2 lower and 2 upper case letter)
# month: number
# day: number
# year: number
# type: string (in = income, out = outcome)
# amount: number (dollar)


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


# start this module by a module menu like the main menu
# user need to go back to the main menu from here
# we need to reach the default and the special functions of this module from the module menu
#
def start_module():
    file_name = current_file_path + "/items.csv"
    table = data_manager.get_table_from_file(file_name)
    options = ["Show table",
               "Add a new item",
               "Remove by ID",
               "Update item by ID",
               "SPECIAL: Year with highest profit",
               "SPECIAL: Average profit per item"]

    while True:

        ui.print_menu("Accounting menu", options, "Back to main menu")
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
                inputs = ui.get_inputs(["Please enter the customer ID you want to delete: "], "")
                table = remove(table, inputs[0])
                if table is not None:
                    data_manager.write_table_to_file(file_name, table)
            elif option == "4":
                inputs = ui.get_inputs(["Please enter the customer ID you want to update: "], "")
                table = update(table, inputs[0])
                if table is not None:
                    data_manager.write_table_to_file(file_name, table)
            elif option == "5":
                ui.print_result(which_year_max(table), "Year on record with max profit")
            elif option == "6":
                avg_amount(table)
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
    title_list = ["ID", "Month", "Day", "Year", "Type", "Amount"]
    ui.print_table(table, title_list)


# Ask a new record as an input from the user than add it to @table, than return @table
#
# @table: list of lists
def add(table):
    MONTH_INDEX = 0
    DAY_INDEX = 1
    YEAR_INDEX = 2
    TYPE_INDEX = 3
    AMOUNT_INDEX = 4
    validity_checklist = [False, False, False]
    validated_entry = [common.generate_random(table)]
    title = "Add accounting entry to table"
    entry_parameters = ["Please enter month (1-12): ",
                        "Please enter the day (1-31): ",
                        "Please enter the year: ",
                        "Please enter the type of entry: ",
                        "Please enter the amount:"]
    while False in validity_checklist:  # Loop asking for input, until input passes every test.
        new_entry = ui.get_inputs(entry_parameters, title)

        # Check if the 3 date inputs for a valid date, if not, print error message.
        try:
            common.check_date_for_validity(int(new_entry[YEAR_INDEX]), int(new_entry[MONTH_INDEX]), int(new_entry[DAY_INDEX]))
        except (ValueError, TypeError) as err:
            ui.print_error_message(err)
        else:
            validity_checklist[0] = True  # if date is valid, mark one validity test passed.

        # Type must be either "in" or "out", if true, mark second test as passed.
        if new_entry[TYPE_INDEX] == "in" or new_entry[TYPE_INDEX] == "out":
            validity_checklist[1] = True
        elif new_entry[TYPE_INDEX] != "in" or new_entry[TYPE_INDEX] != "out":
            ui.print_error_message('Type parameter is incorrect. Must be either "in" or "out".')

        # Test if amount is valid, not, print error message, if yes, mark third test as passed.
        try:
            new_entry[AMOUNT_INDEX] = int(new_entry[AMOUNT_INDEX])
        except ValueError as err:
            ui.print_error_message(err)
        else:
            validity_checklist[2] = True

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
    MONTH_INDEX = 1
    DAY_INDEX = 2
    YEAR_INDEX = 3
    TYPE_INDEX = 4
    AMOUNT_INDEX = 5

    line_to_update_index = None
    for index, line in enumerate(table):
        if line[ID_INDEX] == id_[0]:
            line_to_update_index = table[index]

    if line_to_update_index is None:
        ui.print_error_message("No such ID exists in table.")
        return table

    validity_checklist = [False, False, False]
    title = "Add accounting entry to table"
    entry_parameters = ["Enter updated month, old value was {0}: ".format(table[line_to_update_index][MONTH_INDEX]),
                        "Enter updated day, old value was {0}: ".format(table[line_to_update_index][DAY_INDEX]),
                        "Enter updated year, old value was {0}: ".format(table[line_to_update_index][YEAR_INDEX]),
                        "Enter updated type, old value was {0}: ".format(table[line_to_update_index][TYPE_INDEX]),
                        "Enter updated amount, old value was {0}: ".format(table[line_to_update_index][AMOUNT_INDEX])]
    while False in validity_checklist:  # Loop asking for input, until input passes every test.
        new_entry = id_
        new_entry.extend(ui.get_inputs(entry_parameters, title))

        # Check if the 3 date inputs for a valid date, if not, print error message.
        try:
            common.check_date_for_validity(int(new_entry[YEAR_INDEX]), int(new_entry[MONTH_INDEX]), int(new_entry[DAY_INDEX]))
        except (ValueError, TypeError) as err:
            ui.print_error_message(err)
        else:
            validity_checklist[0] = True  # if date is valid, mark one validity test passed.

        # Type must be either "in" or "out", if true, mark second test as passed.
        if new_entry[TYPE_INDEX] == "in" or new_entry[TYPE_INDEX] == "out":
            validity_checklist[1] = True
        elif new_entry[TYPE_INDEX] != "in" or new_entry[TYPE_INDEX] != "out":
            ui.print_error_message('Type parameter is incorrect. Must be either "in" or "out".')

        # Test if amount is valid, not, print error message, if yes, mark third test as passed.
        try:
            new_entry[AMOUNT_INDEX] = int(new_entry[AMOUNT_INDEX])
        except ValueError as err:
            ui.print_error_message(err)
        else:
            validity_checklist[2] = True

    for index in range(1, len(table[line_to_update_index])):
        table[line_to_update_index][index] = str(new_entry[index])

    return table


# special functions:
# ------------------

# the question: Which year has the highest profit? (profit=in-out)
# return the answer (number)
def which_year_max(table):
    ID_INDEX = 0
    MONTH_INDEX = 1
    DAY_INDEX = 2
    YEAR_INDEX = 3
    TYPE_INDEX = 4
    AMOUNT_INDEX = 5

    year_with_profit = []
    set_of_years = set()
    list_of_years = []
    max_profit_year = 0
    max_profit_amount = 0
    for value in table:
        set_of_years.add(value[YEAR_INDEX])

    list_of_years = list(set_of_years)

    for year in list_of_years:
        year_with_profit.append([year, 0])

    for entry in table:
        for index, year in enumerate(year_with_profit):
            if entry[YEAR_INDEX] == year_with_profit[index][0]:
                if entry[TYPE_INDEX] == "in":
                    year_with_profit[index][1] += int(entry[AMOUNT_INDEX])
                elif entry[TYPE_INDEX] == "out":
                    year_with_profit[index][1] -= int(entry[AMOUNT_INDEX])

    for year_data in year_with_profit:
        if int(year_data[1]) > max_profit_amount:
            max_profit_amount = int(year_data[1])
            max_profit_year = year_data[0]

    return int(max_profit_year)


# the question: What is the average (per item) profit in a given year? [(profit)/(items count) ]
# return the answer (number)
def avg_amount(table, year):
    ID_INDEX = 0
    MONTH_INDEX = 1
    DAY_INDEX = 2
    YEAR_INDEX = 3
    TYPE_INDEX = 4
    AMOUNT_INDEX = 5

    profit = 0
    items_count = 0
    avg_amount_per_item = 0

    for entry in table:
        if entry[YEAR_INDEX] == year:
            if entry[TYPE_INDEX] == "in":
                profit += entry[AMOUNT_INDEX]
                items_count += 1
            if entry[TYPE_INDEX] == "out":
                profit -= entry[AMOUNT_INDEX]

    try:
        avg_amount_per_item = (profit / items_count)
    except ZeroDivisionError as err:
            ui.print_error_message(err)
    
    return avg_amount_per_item
