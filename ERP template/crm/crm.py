# data structure:
# id: string
#     Unique and random generated (at least 2 special char()expect: ';'), 2 number, 2 lower and 2 upper case letter)
# name: string
# email: string
# subscribed: boolean (Is she/he subscribed to the newsletter? 1/0 = yes/not)


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
    file_name = current_file_path + "/customers.csv"
    table = data_manager.get_table_from_file(file_name)
    options = ["Show table",
               "Add a new item",
               "Remove item by ID",
               "Update item by ID",
               "SPECIAL: ID of the Customer with the longest Name",
               "SPECIAL: Customers subscribed to newsletter"]
    while True:
        try:
            ui.print_menu("Customer Relationship Management (CRM) Menu", options, "Back to main menu")
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
                label = "Customer with longest name"
                result = get_longest_name_id(table)
                ui.print_result(result, label)
            elif option == "6":
                label = "Subscribed customers"
                result = get_subscribed_emails(table)
                ui.print_result(result, label)
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
    title_list = ["ID", "Name of Customer", "E-mail address", "Subscribed"]
    ui.print_table(table, title_list)


# Ask a new record as an input from the user than add it to @table, than return @table
#
# @table: list of lists
def add(table):
    # input from user
    title = "Add a customer to table"
    questions = ["Please enter the Name of Customer: ", "Please enter the E-mail address: ", "Please enter whether the customer Subscribed: "]
    new_customer_data = ui.get_inputs(questions, title)

    # adding customer ID to the new customer data
    id_ = common.generate_random(table)
    new_customer_data.insert(0, id_)
    table.append(new_customer_data)
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

    line_to_update = [index for index, line in enumerate(table) if id_ == line[ID_INDEX]]
    if not line_to_update:
        ui.print_error_message("There is no such ID in the table.")
    else:
        title = "Update the data of the customer"
        questions = ["Enter updated Customer Name: ", "Enter updated E-mail address: ", "Enter updated Subscribed data: "]
        new_customer_data = ui.get_inputs(questions, title)
        new_customer_data.insert(ID_INDEX, id_)
        table[int(line_to_update[0])] = new_customer_data
        return table


# special functions:
# ------------------


# the question: What is the id of the customer with the longest name ?
# return type: string (id) - if there are more than one longest name, return the first of descending alphabetical order
def get_longest_name_id(table):
    ID_INDEX = 0
    NAME_INDEX = 1
    current_names = []
    length = 0
    # Get longest name
    for i, j in enumerate(table):
        if len(j[NAME_INDEX]) > length:
            del current_names[:]
            length = len(j[NAME_INDEX])
            current_names.append(j[NAME_INDEX])
        elif len(j[NAME_INDEX]) == length:
            length = len(j[NAME_INDEX])
            current_names.append(j[NAME_INDEX])
    # Get the descending order of the longest names
    switched = True
    while switched:
        counter = 0
        for i in range(len(current_names)-1):
            direction = current_names[i].lower() < current_names[i+1].lower()
            if direction:
                tmp = current_names[i]
                current_names[i] = current_names[i+1]
                current_names[i+1] = tmp
                counter += 1
        if counter == 0:
            switched = False
    # Get the ID of the customer with longest name
    for i, j in enumerate(table):
        if current_names[0] in j:
            return j[ID_INDEX]


# the question: Which customers has subscribed to the newsletter?
# return type: list of string (where string is like email+separator+name, separator=";")
def get_subscribed_emails(table):
    subscribed_customers = []
    for i, j in enumerate(table):
        if int(j[3]) == 1:
            email = j[2]
            name = j[1]
            subscribed_customers.append(email + " ; " + name)
    return subscribed_customers

