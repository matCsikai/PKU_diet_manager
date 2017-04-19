import csv


def import_csv_file(file_name="food_database.csv"):
    database_as_list = []
    with open(file_name, newline="") as csv_file:
        imported_database = csv.reader(csv_file, delimiter=',', quotechar="|")
        for row in imported_database:
            database_as_list.append(str(row))
    return database_as_list


# read file into a @table
#
# @file_name: string
# @table: list of lists of strings
def get_table_from_file(file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()
    table = [element.replace("\n", "").split(";") for element in lines]
    return table


# write a @table into a file
#
# @file_name: string
# @table: list of lists of strings
def write_table_to_file(file_name, table):
    with open(file_name, "w") as file:
        for record in table:
            row = ';'.join(record)
            file.write(row + "\n")
