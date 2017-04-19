# importing everything you need
import os
from importlib.machinery import SourceFileLoader
current_file_path = os.path.dirname(os.path.abspath(__file__))
# User interface module
ui = SourceFileLoader("ui", current_file_path + "/ui.py").load_module()
# data manager module
data_manager = SourceFileLoader("data_manager", current_file_path + "/data_manager.py").load_module()
# common module
common = SourceFileLoader("common", current_file_path + "/common.py").load_module()


def start_module(tolerance):
    options = ["Enter your PHA tolerance", "Your current tolerance"]
    while True:
        ui.print_menu("Tolerance level menu", options, "Back to main menu")
        try:
            inputs = ui.get_inputs(["Please enter a number: "], "")
            option = inputs[0]
            if option == "1":
                tolerance = ui.get_inputs(["Please enter your PHA tolerance level: "], "")
                while True:
                    if not common.is_int(tolerance):
                        tolerance = ui.get_inputs(["Please enter your PHA tolerance level: "], "")
                    elif int(tolerance) < 20 or int(tolerance) > 5000:
                        tolerance = ui.get_inputs(["Please enter your PHA tolerance level as an integer between 20 and 5000 mg: "], "")
                    else:
                        break

            elif option == "2":
                ui.print_result(tolerance, "Your current PHA tolerance")
            elif option == "0":
                break
            else:
                raise KeyError("There is no such option.")
        except KeyError as err:
            ui.print_error_message(err)