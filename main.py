#import sys
#import os
#import common
#import ui  # User Interface
#from importlib.machinery import SourceFileLoader
import json
from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
import werkzeug.security
import requests
import data_manager
from datetime import datetime

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

app.secret_key = 'A0Zr98j/3yX R~XHa!jmN]LWX/,?RT'

@app.route('/')
def index():
    user_data = get_user_data()
    return render_template('index.html', loggedin=user_data["loggedin"], username=user_data["username"], user_id=user_data["user_id"])


def get_user_data():
    loggedin = False
    username = ""
    user_id = ""
    if 'username' in session:
        loggedin = True
        username = session['username']
        get_id_query = """SELECT id FROM diet_users WHERE username=%s"""
        data = (username, )
        result = data_manager.handle_database(get_id_query, data)
        user_id = result['rows'][0][0]
    return {"loggedin": loggedin, "username": username, "user_id": user_id}

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
            food_query = 'http://api.nal.usda.gov/ndb/nutrients/?format=json&api_key=' + API_KEY + '&nutrients=508&ndbno='+ ndbno
            food_response = requests.get(food_query)
            if food_response.status_code == 200:
                results = food_response.json()
                if results['report']['total'] != 0:
                    result_list.append(result)
    else:
        return render_template('error.html', error='Error handling data. Try again!')
    user_data = get_user_data()
    return render_template('search.html', results=result_list, loggedin=user_data["loggedin"], username=user_data["username"], user_id=user_data["user_id"])


@app.route('/food')
def food():
    ndbno = request.args.get('ndbno')
    query = 'http://api.nal.usda.gov/ndb/nutrients/?format=json&api_key=' + API_KEY + '&nutrients=508&ndbno='+ ndbno # query = url_to_api
    response = requests.get(query)
    if response.status_code == 200:
        result = response.json()
        name = result['report']['foods'][0]['name']
        nutrients = result['report']['foods'][0]['nutrients'][0]
        nutrient_id = nutrients['nutrient_id']
        unit = nutrients['unit']
        gm = nutrients['gm']
        value = nutrients['value']
        nutrient = nutrients['nutrient']
    else:
        return render_template('error.html', error='Error handling data. Try again!')
    user_data = get_user_data()
    return render_template('food.html', name=name, nutrient=nutrient, gm=gm, loggedin=user_data["loggedin"], username=user_data["username"], user_id=user_data["user_id"])

""""""


@app.route('/registration')
def registration():
    return render_template('registration.html')


@app.route('/registration/new', methods=['POST'])
def add_new_registration():
    tolerance = request.form['tolerance']
    new_username = request.form['new_user_name']
    new_password = request.form['new_password']
    username_check_query = """SELECT username FROM diet_users WHERE username=%s"""
    data = (new_username, )
    result = data_manager.handle_query(username_check_query, data)
    if result['result'] == 'success':
        if result['row_count'] == 0:
            if request.form['new_password'] != request.form['confirm_password']:
                flash('Password confirmation failed. Please re-enter password!')
                return render_template('registration.html', username=new_username)
            else:
                hashed_password = werkzeug.security.generate_password_hash(new_password, method='pbkdf2:sha256',
                                                                           salt_length=8)
                query = """INSERT INTO diet_users (username, password, submission_time, tolerance) VALUES (%s, %s, %s, %s)"""
                submission_time = str(datetime.now())[:-7]
                data = (new_username, hashed_password, submission_time, tolerance)
                insert_check_result = data_manager.handle_query(query, data)
                if insert_check_result['result'] == 'success':
                    insert_check_query = """SELECT username FROM diet_users WHERE username = %s"""
                    data = (new_username, )
                    result = data_manager.handle_database(insert_check_query, data)
                    if result:
                        info = True
                        return render_template('registration.html', info=info)
                    else:
                        return render_template('error.html', error=result['result'])
                else:
                    return render_template('error.html', error=result['result'])
        else:
            flash('Username already in database! Choose another username')
            return redirect(url_for('registration'))
    else:
        return render_template('error.html', error=result['result'])
    return redirect('/')


@app.route('/login', methods=['GET'])
def get_login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def post_login():
    user_name = request.form['user_name']
    password = request.form['password']
    get_user_query = """SELECT id, username, password FROM diet_users WHERE username=%s"""
    data = (user_name, )
    user = data_manager.handle_query(get_user_query, data)
    if user['result'] == 'success':
        if user['row_count'] != 0:
            if werkzeug.security.check_password_hash(user['rows'][0][2], password):
                session['username'] = user_name
                return redirect('/')
            else:
                flash('Authentification failed. Try to login again!')
                return redirect(url_for('get_login'))
        else:
            flash('Username not registered. Try to login again!')
            return redirect(url_for('get_login'))
    else:
        return render_template('error.html', error=user['result'])


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


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