

import sys
import os
import ui  # User Interface
from importlib.machinery import SourceFileLoader
main_path = os.path.dirname(os.path.abspath(__file__))
# Tolerance input
tolerance_input = SourceFileLoader("tolerance_input", "tolerance_input.py").load_module()
# My recipes
my_recipes = SourceFileLoader("my_recipes", "my_recipes.py").load_module()
# Daily menu
daily_menu = SourceFileLoader("daily_menu", "daily_menu.py").load_module()


def choose():
    inputs = ui.get_inputs(["Please enter a number: "], "")
    option = inputs[0]
    tolerance = 500
    if option == "1":
        tolerance = tolerance_input.start_module(tolerance)
    elif option == "2":
        my_recipes.start_module(tolerance)
    elif option == "3":
        daily_menu.start_module(tolerance)
    elif option == "0":
        sys.exit(0)
    else:
        raise KeyError("There is no such option.")


def handle_menu():
    options = ["Tolerance input",
               "My recipes",
               "Daily menu"]

    ui.print_menu("Main menu", options, "Exit program")


def main():
    usa_database = data_manager.import_csv_file()
    while True:
        handle_menu()
        try:
            choose()
        except KeyError as err:
            ui.print_error_message(err)


if __name__ == '__main__':
    main()
