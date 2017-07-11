from flask import Flask, render_template, redirect, request
import sys
import os
import data_manager
import common
import ui  # User Interface
from importlib.machinery import SourceFileLoader
import requests
import json

'''
main_path = os.path.dirname(os.path.abspath(__file__))
# Tolerance input
tolerance_input = SourceFileLoader("tolerance_input", "tolerance_input.py").load_module()
# My recipes
my_recipes = SourceFileLoader("my_recipes", "my_recipes.py").load_module()
# Daily menu
daily_menu = SourceFileLoader("daily_menu", "daily_menu.py").load_module()
'''


app = Flask(__name__)
API_KEY = 'AQ1fP3DgzdClqCBGxKFRCfrXu5yrjBJNFwBdfUIb'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    search = request.args.get('search')
    query = 'https://api.nal.usda.gov/ndb/search/?format=json&q=' + search + '&sort=n&max=25&offset=0&api_key=' + API_KEY
    response = requests.get(query)
    if response.status_code == 200:
        results = response.json()
        result_list = []
        for result in results['list']['item']:
            ndbno = result['ndbno']
            query = 'http://api.nal.usda.gov/ndb/nutrients/?format=json&api_key=' + API_KEY + '&nutrients=508&ndbno='+ ndbno
            response = requests.get(query)
            if response.status_code == 200:
                results = response.json()
                if results['report']['total'] != 0:
                    result_list.append(result)
    else:
        return render_template('error.html', error='Error handling data. Try again!')
    return render_template('search.html', results=result_list)


@app.route('/food')
def food():
    ndbno = request.args.get('ndbno')
    query = 'http://api.nal.usda.gov/ndb/nutrients/?format=json&api_key=' + API_KEY + '&nutrients=508&ndbno='+ ndbno
    response = requests.get(query)
    if response.status_code == 200:
        result = response.json()
        name = result['report']['foods'][0]['name']
        nutrients = result['report']['foods'][0]['nutrients'][0]
        print(nutrients)
        nutrient_id = nutrients['nutrient_id']
        unit = nutrients['unit']
        gm = nutrients['gm']
        value = nutrients['value']
        nutrient = nutrients['nutrient']
    else:
        return render_template('error.html', error='Error handling data. Try again!')
    return render_template('food.html', name=name, nutrient=nutrient, value=value, unit=unit)

if __name__ == '__main__':
    app.run(debug=True)

'''
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
    elif option == "4":
        common.handle_database_menu()
    elif option == "0":
        sys.exit(0)
    else:
        raise KeyError("There is no such option.")


def handle_menu():
    options = ["Tolerance input",
               "My recipes",
               "Daily menu",
               "Search database"]

    ui.print_menu("Main menu", options, "Exit program")





def main():
    while True:
        handle_menu()
        try:
            choose()
        except KeyError as err:
            ui.print_error_message(err)


if __name__ == '__main__':
    main()
'''