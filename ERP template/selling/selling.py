# data structure:
# id: string
#     Unique and random generated (at least 2 special char()expect: ';'), 2 number, 2 lower and 2 upper case letter)
# title: string
# price: number (the actual selling price in $)
# month: number
# day: number
# year: number
# month,year and day combined gives the date the purchase was made


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

    # you code
    # call ui.print_menu(title, list_options, exit_message):
    # @title: string - title of the menu (Selling)
    # @list_options: list of strings - the options in the menu
    # @exit_message: string - the last option with (0) (example: "Back to main menu")
    # This function needs to generate outputs like this:
    # Selling:
    # (1) Show table
    # (2) Add
    # (3) Remove
    # (4) Update
    # (5) get_lowest_price_item_id
    # (6) get_items_sold_between
    # (0) Back to main menu

    file_name = current_file_path + "/sellings.csv"
    table = data_manager.get_table_from_file(file_name)
    options = ["Show table",
               "Add a new item",
               "Remove by ID",
               "Update item by ID",
               "SPECIAL: Get lowest price item ID",
               "SPECIAL: Get items sold between"]

    while True:
        ui.print_menu("Selling menu", options, "Back to main menu")
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
                get_lowest_price_item_id(table)
            elif option == "6":
                # month_from, day_from, year_from, month_to, day_to, year_to
                get_items_sold_between(table, month_from, day_from, year_from, month_to, day_to, year_to)
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
    title_list = ["id", "title", "price", "month", "day", "year"]
    ui.print_table(table, title_list)


# Ask a new record as an input from the user than add it to @table, than return @table
#
# @table: list of lists
def add(table):
    id = common.generate_random(table)
    title = "To add a new record, enter the following parameters: "
    list_labels = ["Title: ", "Price: ", "Month: ", "Day: ", "Year: "]
    new_record_list = ui.get_inputs(list_labels, title)
    # Check if numeric data was provided to Price, Month, Day and Year
    validate_user_entry(new_record_list)
    new_record_list.insert(0, id)
    table.append(new_record_list)
    data_manager.write_table_to_file(current_file_path + "/sellings.csv", table)
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
    PRICE_INDEX = 2
    MONTH_INDEX = 3
    DAY_INDEX = 4
    YEAR_INDEX = 5

    line_to_update_index = None
    for index, line in enumerate(table):
        if line[ID_INDEX] == id_[0]:
            line_to_update_index = table[index]

    if line_to_update_index is None:
        ui.print_error_message("No such ID exists in table.")
        return table

    validity_checklist = [False, False]
    title = "Add selling entry to table"
    entry_parameters = ["Enter updated title, old value was {0}: ".format(table[line_to_update_index][TITLE_INDEX]),
                        "Enter updated price, old value was {0}: ".format(table[line_to_update_index][PRICE_INDEX]),
                        "Enter updated month, old value was {0}: ".format(table[line_to_update_index][MONTH_INDEX]),
                        "Enter updated day, old value was {0}: ".format(table[line_to_update_index][DAY_INDEX]),
                        "Enter updated year, old value was {0}: ".format(table[line_to_update_index][YEAR_INDEX])]
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

        # Test if price is valid, if not, print error message, if yes, mark test as passed.
        try:
            new_entry[PRICE_INDEX] = int(new_entry[PRICE_INDEX])
        except ValueError as err:
            ui.print_error_message(err)
        else:
            validity_checklist[1] = True

    for index in range(1, len(table[line_to_update_index])):
        table[line_to_update_index][index] = str(new_entry[index])
    data_manager.write_table_to_file(current_file_path + "/sellings.csv", table)
    return table


# special functions:
# ------------------

# the question: What is the id of the item that sold for the lowest price ?
# return type: string (id)
# if there are more than one with the lowest price, return the first of descending alphabetical order
def get_lowest_price_item_id(table):
    lowest_price = min(int(i[2]) for i in table)
    result_list = []
    for i in table:
        if int(i[2]) == lowest_price:
            result_list.append(i[0])
    if len(result_list) == 1:
        ui.print_result(result_list[0], "The ID of the lowest price item is")
        return result_list[0]
    else:
        ui.print_result(result_list, "The IDs of the lowest price item are")
        return result_list

# the question: Which items are sold between two given dates ? (from_date < birth_date < to_date)
# return type: list of lists (the filtered table)
def get_items_sold_between(table, month_from, day_from, year_from, month_to, day_to, year_to):

    # your code

    pass


def validate_user_entry(new_record_list):
    if not common.is_int(new_record_list[1]):
        ui.print_error_message("Price should be numeric")
        start_module()
    if not common.is_int(new_record_list[2]):
        ui.print_error_message("Month should be numeric")
        start_module()
    if not common.is_int(new_record_list[3]):
        ui.print_error_message("Day should be numeric")
        start_module()
    if not common.is_int(new_record_list[4]):
        ui.print_error_message("Year should be numeric")
        start_module()
    # Check if the 3 date inputs for a valid date, if not, print error message.
    try:
        common.check_date_for_validity(int(new_record_list[4]), int(new_record_list[2]), int(new_record_list[3]))
    except (ValueError, TypeError):
        ui.print_error_message("The provided date is not valid, please try again")
        start_module()