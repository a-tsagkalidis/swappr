import re
import sqlite3
from functools import wraps
from flask import redirect, session


# |----- SQL DATABASE HELPING FUNCTIONS ----| 
def cursor_execute(query, *args):
    '''
    Executes a SQL query even if it has a variable number of arguments
    '''
    conn = sqlite3.connect('swappr.db')
    cursor = conn.cursor()
    cursor.execute(query, args)
    conn.commit()
    conn.close()


def cursor_fetch(query, *args):
    '''
    Fetches data from the database in two tuples, where the
    first one has the columns and the second has the values.
    Then it converts them into a json style data structure
    with key/value dict logic.
    '''
    conn = sqlite3.connect('swappr.db')
    cursor = conn.cursor()
    cursor.execute(query, args)

    fetched_data_tuples = cursor.fetchall()
    fetched_data_json = []
    for fetched_data_tuple in fetched_data_tuples:
        fetched_data_json.append(
            tuples_to_dict(
                cursor.description,
                fetched_data_tuple
            )
        )
    conn.close()
    return fetched_data_json


def tuples_to_dict(keys_tuple, values_tuple):
    '''
    Converts two tuples into one dictionary
    '''
    if values_tuple:
        values = values_tuple
        keys = [key[0] for key in keys_tuple]
        return dict(zip(keys, values))
    else:
        return None


# |----- SIGNUP/ACCOUNT HELPING FUNCTIONS ----| 
def strong_password(password):
    '''
    Checks if a password is strong enough. To return `True` the password
    should contain at least one upper case letter, one lower case letter,
    one decimal number, and one punctuation character, while its length
    must be at least of eight characters - else returns `False`.
    '''
    password_regex_stipulations = re.compile(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[\w!@#$%^&*()_+]{8,}$'
    )
    return bool(password_regex_stipulations.match(password))


def email_exists(email):
    '''
    Fetches user input email from the database to validate
    its existence. In case email is not found, return None.
    '''
    conn = sqlite3.connect('swappr.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM users WHERE email = ?',
        (email,)
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None


def username_exists(username, *args):
    '''
    Fetches user input username from the database to validate
    its existence. If username is not found, return None.
    In case of update_username the function gets user_id in *args
    so that it can check existent usernames excluding the one
    of the connected user. 
    '''
    conn = sqlite3.connect('swappr.db')
    cursor = conn.cursor()
    if not args:
        cursor.execute(
            'SELECT * FROM users WHERE username = ?',
            (username,)
        )
    else:
        cursor.execute(
            'SELECT * FROM users WHERE username = ? AND id != ?',
            (
                username,
                *args,
            )
        )
    result = cursor.fetchone()
    conn.close()
    return result is not None


# |----- SUBMIT/EDIT-SUBMISSION HELPING FUNCTIONS ----| 
def get_list_of_values(json_data, column_name):
    '''
    Converts a json file into a list with values of
    the selected column
    '''
    return [item[column_name] for item in json_data]


def check_submitted_location(submitted_value, valid_values, error_message):
    '''
    Checks if a user's submitted value is actually
    stored in the database
    '''
    if submitted_value not in valid_values:
        raise ValueError(error_message)


# |----- ROUTING HELPING FUNCTIONS ----| 
def login_required(f):
    """
    Decorate routes to require login
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/signin")
        return f(*args, **kwargs)
    return decorated_function


def comma(integer):
    '''
    Formats an integer by placing commas between thousands
    '''
    return f"{integer:,}"


def whitespace(text):
    '''
    Formats a snakecase string into a readable title by replacing
    underscores with whitespaces and initial lowercase letters with
    capital ones
    '''
    return text.replace('_', ' ').title()
