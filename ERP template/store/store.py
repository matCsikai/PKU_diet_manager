# data structure:
# id: string
#     Unique and random generated (at least 2 special char()expect: ';'), 2 number, 2 lower and 2 upper case letter)
# title: string
# manufacturer: string
# price: number (dollar)
# in_stock: number


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
    file_name = current_file_path + "/games.csv"
    table = data_manager.get_table_from_file(file_name)
    options = ["Show table",
               "Add a new item",
               "Remove by ID",
               "Update item by ID",
               "SPECIAL: Get counts by manufacturers",
               "SPECIAL: Get average by manufacturer"]

    while True:
        ui.print_menu("Store menu", options, "Back to main menu")
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
                inputs = ui.get_inputs(["Please enter the product ID you want to delete: "], "")
                table = remove(table, inputs[0])
                if table is not None:
                    data_manager.write_table_to_file(file_name, table)
            elif option == "4":
                inputs = ui.get_inputs(["Please enter the product ID you want to update: "], "")
                table = update(table, inputs[0])
                if table is not None:
                    data_manager.write_table_to_file(file_name, table)
            elif option == "5":
                get_counts_by_manufacturers(table)
            elif option == "6":
                manufacturer = ui.get_inputs(["Please enter manufacturer's name: "], "")[0]
                get_average_by_manufacturer(table, manufacturer)
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
    title_list = ["id", "title", "manufacturer", "price", "in_stock"]
    ui.print_table(table, title_list)


# Ask a new record as an input from the user than add it to @table, than return @table
#
# @table: list of lists
def add(table):
    id = common.generate_random(table)
    title = "To add a new record, enter the following parameters: "
    list_labels = ["Title: ", "Manufacturer: ", "Price: ", "In_stock: "]
    new_record_list = ui.get_inputs(list_labels, title)
    # Check if numeric data was provided to Price and In_stock
    validate_user_entry(new_record_list)
    new_record_list.insert(0, id)
    table.append(new_record_list)
    # data_manager.write_table_to_file(current_file_path + "/sellings.csv", table)
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
    TITLE_INDEX = 1
    MANUFACTURER_INDEX = 2
    PRICE_INDEX = 3
    IN_STOCK_INDEX = 4

    line_to_update_index = None
    for index, line in enumerate(table):
        if line[ID_INDEX] == id_[0]:
            line_to_update_index = table[index]

    if line_to_update_index is None:
        ui.print_error_message("No such ID exists in table.")
        return table

    validity_checklist = [False, False]
    title = "Add store entry to table"
    entry_parameters = ["Enter updated title, old value was {0}: ".format(table[line_to_update_index][TITLE_INDEX]),
                        "Enter updated manufacturer, old value was {0}: ".format(table[line_to_update_index][MANUFACTURER_INDEX]),
                        "Enter updated price, old value was {0}: ".format(table[line_to_update_index][PRICE_INDEX]),
                        "Enter updated in_stock value, old value was {0}: ".format(table[line_to_update_index][IN_STOCK_INDEX])]
    while False in validity_checklist:  # Loop asking for input, until input passes every test.
        new_entry = id_
        new_entry.extend(ui.get_inputs(entry_parameters, title))

        # Test if price is valid, if not, print error message, if yes, mark test as passed.
        try:
            new_entry[PRICE_INDEX] = int(new_entry[PRICE_INDEX])
        except ValueError as err:
            ui.print_error_message(err)
        else:
            validity_checklist[0] = True

        # Test if in_stock value is valid, if not, print error message, if yes, mark test as passed.
        try:
            new_entry[IN_STOCK_INDEX] = int(new_entry[IN_STOCK_INDEX])
        except ValueError as err:
            ui.print_error_message(err)
        else:
            validity_checklist[1] = True

    for index in range(1, len(table[line_to_update_index])):
        table[line_to_update_index][index] = str(new_entry[index])
    # data_manager.write_table_to_file(current_file_path + "/games.csv", table)
    return table


# special functions:
# ------------------

# the question: How many different kinds of game are available of each manufacturer?
# return type: a dictionary with this structure: { [manufacturer] : [count] }
def get_counts_by_manufacturers(table):
    return_dict = {}
    for i in table:
        if i[2] in return_dict:
            return_dict[i[2]] += 1
        else:
            return_dict[i[2]] = 1
    ui.print_result(return_dict, "Counts by manufacturers: ")
    return return_dict


# the question: What is the average amount of games in stock of a given manufacturer?
# return type: number
def get_average_by_manufacturer(table, manufacturer):
    sum_amount_of_games = 0
    count_manufacturer = 0
    for i in table:
        if i[2] == manufacturer:
            if common.is_int(i[4]):
                sum_amount_of_games += int(i[4])
                count_manufacturer += 1
    if count_manufacturer == 0:
        ui.print_error_message("Invalid manufacturer name")
        return 0
    ui.print_result(sum_amount_of_games / count_manufacturer, "Average amount of games in stock of {0}: ".format(manufacturer))
    return sum_amount_of_games / count_manufacturer


def validate_user_entry(new_record_list):
    if not common.is_int(new_record_list[2]):
        ui.print_error_message("Price should be numeric")
        start_module()
    if not common.is_int(new_record_list[3]):
        ui.print_error_message("In-stock should be numeric")
        start_module()
