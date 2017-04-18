

# This function needs to print outputs like this:
# /-----------------------------------\
# |   id   |      title     |  type   |
# |--------|----------------|---------|
# |   0    | Counter strike |    fps  |
# |--------|----------------|---------|
# |   1    |       fo       |    fps  |
# \-----------------------------------/
#
# @table: list of lists - the table to print out
# @title_list: list of strings - the head of the table
def print_table(table, title_list):
    cell_min_length = 8

    max_cell_length = list(0 for _ in range(len(title_list)))
    for n, cell in enumerate(title_list):
        if max_cell_length[n] < len(cell):
            max_cell_length[n] = len(cell)
    for i, row in enumerate(table):
        for n, cell in enumerate(row):
            if max_cell_length[n] < len(cell):
                max_cell_length[n] = len(cell)

    sum_max_cell_length = 0
    for i in max_cell_length:
        sum_max_cell_length += i

    print("/", end="")
    print("-" * (sum_max_cell_length + len(max_cell_length)*2 + len(row) - 1), end="")
    print("\\")
    for i, n in enumerate(title_list):
        print("|" + n.center(max_cell_length[i]+2), end="")
    print("|")

    for row in table:
        print("|", end="")
        for i, cell in enumerate(row):
            print("-" * (max_cell_length[i]+2), end="|")
        print()
        for i, cell in enumerate(row):
            print("|" + cell.center(max_cell_length[i]+2), end="")
        print("|")
    print("\\", end="")
    print("-" * (sum_max_cell_length + len(max_cell_length)*2 + len(row) - 1), end="")
    print("/")


# This function needs to print result of the special functions
#
# @result: string or list or dictionary - result of the special function
# @label: string - label of the result
def print_result(result, label):
    print(label)
    if isinstance(result, str) or isinstance(result, int) or isinstance(result, float):
        print(result)
    elif isinstance(result, list) or isinstance(result, tuple) or isinstance(result, set):
        for element in result:
            print(element)
    elif isinstance(result, dict):
        for key, value in result.items():
            print("{0}: {1}".format(key, value))


# This function needs to generate outputs like this:
# Main menu:
# (1) Store manager
# (2) Human resources manager
# (3) Inventory manager
# (4) Accounting manager
# (5) Selling manager
# (6) Customer relationship management (CRM)
# (0) Exit program
#
# @title: string - title of the menu
# @list_options: list of strings - the options in the menu
# @exit_message: string - the last option with (0) (example: "Back to main menu")
def print_menu(title, list_options, exit_message):
    print(title)
    for option in enumerate(list_options):
        print("({0}) {1}".format(option[0] + 1, option[1]))
    print("({0}) {1}".format("0", exit_message))


# This function gets a list of inputs from the user by the terminal
#
# @list_labels: list of strings - the labels of the inputs
# @title: string - title of the "input section"
# @inputs: list of string - list of the received values from the user
def get_inputs(list_labels, title):
    inputs = []
    print(title)
    for question in list_labels:
        user_input = input(question)
        inputs.append(user_input)
    return inputs


# This function needs to print an error message. (example: Error: @message)
#
# @message: string - the error message
def print_error_message(message):
    print("Error: {0}".format(message))
    # your code
