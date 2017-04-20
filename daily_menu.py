# data structure:
# id: string
# title: string
# food name: string
# quantity_gram: number
# measure: string (so far...)
# PHA content: number
# Food entry date year: number
# Food entry date month: number
# Food entry date day: number


# importing everything you need
import os
import datetime
from importlib.machinery import SourceFileLoader
current_file_path = os.path.dirname(os.path.abspath(__file__))
# User interface module
ui = SourceFileLoader("ui", current_file_path + "/ui.py").load_module()
# data manager module
data_manager = SourceFileLoader("data_manager", current_file_path + "/data_manager.py").load_module()
# common module
common = SourceFileLoader("common", current_file_path + "/common.py").load_module()


# start this module by a module menu like the main menu
# user need to go back to the main menu from here
# we need to reach the default and the special functions of this module from the module menu
#
def start_module(tolerance):
    file_name = "daily_menu.csv"
    table = data_manager.import_csv_file(file_name)
    for i, v in enumerate(table):
        table[i] = v.replace('[', '').replace(']', '').replace("'", "").split(',')
    
    ID_INDEX = 0
    FOOD_INDEX = 1
    QUANTITY_INDEX = 2
    MEASURE_INDEX = 3
    PHA_CONTENT_INDEX = 4
    YEAR_INDEX = 5
    MONTH_INDEX = 6
    DAY_INDEX = 7
    
    year_today = datetime.datetime.now().year
    month_today = datetime.datetime.now().month
    day_today = datetime.datetime.now().day

    today_table = []
    sum_PHA = 0
    for i in table:
        if year_today == int(i[YEAR_INDEX]) and month_today == int(i[MONTH_INDEX]) and day_today == int(i[DAY_INDEX]):
            today_table.append(i)
            sum_PHA += float(i[PHA_CONTENT_INDEX])

    options = ["Show daily status",
               "Add food item",
               "Remove food item",
               "Update food item",
               "Search in food diary"]

    while True:
        ui.print_menu("Daily menu", options, "Back to main menu")
        try:
            inputs = ui.get_inputs(["Please enter a number: "], "")
            option = inputs[0]
            if option == "1":
                show_table(today_table)
                print("\nYour PHA tolerance is {0} mg.\nYou consumed {1} mg PHA today.\nRemaining PHA today is {2} mg.\n".format(float(tolerance), sum_PHA, tolerance - sum_PHA))
            elif option == "2":
                ui.print_error_message("This function is under constrution")
            elif option == "3":
                ui.print_error_message("This function is under constrution")
            elif option == "4":
                ui.print_error_message("This function is under constrution")
            elif option == "0":
                break
            else:
                raise KeyError("There is no such option.")
        except KeyError as err:
            ui.print_error_message(err)


def show_table(table):
    title_list = ["id", "food name", "quantity (g)", "measure", "PHA content", "year", "month", "day"]
    ui.print_table(table, title_list)