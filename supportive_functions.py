import re
import json
import string
import sqlite3
from loguru import logger
from functools import wraps
from flask import redirect, session
from werkzeug.security import check_password_hash


def cursor_execute(query, *args):
    '''
    Executes a SQL query even if it has a variable number of arguments
    '''
    conn = sqlite3.connect('swappr.db')
    cursor = conn.cursor()
    cursor.execute(query, (args))
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
        fetched_data_json.append(tuples_to_dict(cursor.description, fetched_data_tuple))
    conn.close()
    return fetched_data_json


def create_database_tables():
    '''
    Creates all the needed tables in the database in case
    they do not exist.
    '''
    cursor_execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER NOT NULL,
            email TEXT UNIQUE,
            username TEXT UNIQUE,
            hash TEXT,
            registration_date DATETIME NOT NULL,
            verified_account BOOLEAN NOT NULL,
            PRIMARY KEY (id)
        );
    ''')

    cursor_execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            house_type TEXT NOT NULL,
            square_meters INTEGER NOT NULL,
            rental INTEGER NOT NULL,
            bedrooms INTEGER,
            bathrooms INTEGER,
            city TEXT NOT NULL,
            municipality TEXT NOT NULL,
            region TEXT NOT NULL,
            exposure TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
    ''')

    cursor_execute('''
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY,
            city TEXT UNIQUE NOT NULL
        );
    ''')

    cursor_execute('''
        CREATE TABLE IF NOT EXISTS municipalities (
            id INTEGER PRIMARY KEY,
            municipality TEXT UNIQUE NOT NULL,
            city_id INTEGER,
            FOREIGN KEY (city_id) REFERENCES cities (id)
        );
    ''')

    cursor_execute('''
        CREATE TABLE IF NOT EXISTS regions (
            id INTEGER PRIMARY KEY,
            region TEXT UNIQUE NOT NULL,
            postal_code TEXT NOT NULL, -- Added postal_code column
            municipality_id INTEGER,
            FOREIGN KEY (municipality_id) REFERENCES municipalities (id)
        );
    ''')


def import_locations():
    '''
    Imports any non-existing data from the locations.json in
    the proper relational database tables. Executes when app.py
    runs. Updates app.log with newly imported locations that were
    detected in the JSON file
    '''
    # Declare a variable counter for newly imported locations.
    location_update = {
        'cities': [],
        'municipalities': [],
        'regions': [],
        'cities count': 0,
        'municipalities count': 0,
        'regions count': 0,
        'total new entries': 0
    }

    # Load JSON data from a separate file
    with open('locations.json', 'r') as file:
        locations = json.load(file)

    # Connect to SQLite database
    conn = sqlite3.connect('swappr.db')
    cursor = conn.cursor()

    # Insert data into the 'cities' table
    cities_data = set(location['city'] for location in locations)
    for city in cities_data:
        existing_city = cursor.execute('SELECT id FROM cities WHERE city = ?', (city,)).fetchone()
        if not existing_city:
            location_update['cities'].append(city)
            location_update['cities count'] +=1
            location_update['total new entries'] += 1
            cursor.execute('INSERT INTO cities (city) VALUES (?)', (city,))
    
    # Commit the changes to ensure city IDs are available for foreign key references
    conn.commit()

    # Insert data into the 'municipalities' table
    for location in locations:
        city_id = cursor.execute('SELECT id FROM cities WHERE city = ?', (location['city'],)).fetchone()[0]
        municipality = location['municipality']
        
        # Check if the municipality already exists in the table
        existing_municipality = cursor.execute('SELECT id FROM municipalities WHERE municipality = ?', (municipality,)).fetchone()
        if not existing_municipality:
            location_update['municipalities'].append(municipality)
            location_update['municipalities count'] += 1
            location_update['total new entries'] += 1
            cursor.execute('INSERT INTO municipalities (municipality, city_id) VALUES (?, ?)', (municipality, city_id))

    # Commit the changes to ensure municipality IDs are available for foreign key references
    conn.commit()

    # Insert data into the 'regions' table
    for location in locations:
        municipality_id = cursor.execute('SELECT id FROM municipalities WHERE municipality = ?', (location['municipality'],)).fetchone()[0]
        for region, postal_code in location['region'].items():
            
            # Check if the region already exists in the table
            existing_region = cursor.execute('SELECT id FROM regions WHERE region = ?', (region,)).fetchone()
            if not existing_region:
                location_update['regions'].append(region)
                location_update['regions count'] += 1
                location_update['total new entries'] += 1
                cursor.execute('INSERT INTO regions (region, postal_code, municipality_id) VALUES (?, ?, ?)', (region, postal_code, municipality_id))

    # Commit the final changes and close the connection
    conn.commit()
    conn.close()

    flag = False
    if location_update['cities'] and location_update['municipalities'] and location_update['regions']:
        flag = True

    return location_update, flag


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


def log(message, level='INFO', indent=28):
    message = '\n'.join([' ' * indent + line for line in message.splitlines()])
    logger.log(
        level,
        message,
    )


def login_required(f):
    """
    Decorate routes to require login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/signin")
        return f(*args, **kwargs)
    return decorated_function


def is_strong_password(password):
    '''
    Checks if a password is strong enough. To return `True` the password
    should contain at least one upper case letter, one lower case letter,
    one decimal number, and one punctuation character, while its length
    must be at least of eight characters - else returns `False`.
    '''
    password_regex_stipulations = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[\w!@#$%^&*()_+]{8,}$')
    return bool(password_regex_stipulations.match(password))


def is_email_exists(email):
    '''
    Fetches user input email from the database to validate
    its existence. In case email is not found, return None.
    '''
    conn = sqlite3.connect('swappr.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def is_username_exists(username, *args):
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
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    else:
        cursor.execute('SELECT * FROM users WHERE username = ? AND id != ?', (username, *args,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def signup_validation(email, username, password, confirm_password):
    '''
    Checks for valid user input form in signup route.
    '''
    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 20

    # Ensure fields are not blank
    if not email or not username or not password or not confirm_password:
        raise ValueError("Please fill in all the required fields.")
    
    # Ensure email does not contain invalid email characters and has valid structure
    email_regex_stipulations = re.compile(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    if not email_regex_stipulations.match(email):
        raise ValueError('Please enter a valid email address.')

    # Ensure password and confirmation match
    if password != confirm_password:
        raise ValueError("Password and password confirmation do not match.")

    # Ensure new username does not fall short the minimum length
    if len(username) < MIN_USERNAME_LENGTH:
        raise ValueError(f"Username must be at least {MIN_USERNAME_LENGTH} characters long.")
    
    # Ensure new username does not exceed the maximum length
    if len(username) > MAX_USERNAME_LENGTH:
        raise ValueError(f"Username cannot exceed {MAX_USERNAME_LENGTH} characters.")

    # Ensure username does not contain punctuation characters or whitespaces
    if any(char in string.punctuation or char.isspace() for char in username):
        raise ValueError("Username cannot contain punctuation characters or whitespaces.")

    # # Ensure password is strong
    # if not is_strong_password(password):
    #     raise ValueError(
    #         '''
    #         Password must be at least 8 characters long, including at least 1
    #         uppercase letter, 1 lowercase letter, a decimal number, and a
    #         punctuation character.
    #         '''
    #     )

    # Ensure email does not exist
    if is_email_exists(email):
        raise ValueError("The provided email address is already in use. Please choose a different one.")

    # Ensure username does not exist
    if is_username_exists(username):
        raise ValueError("The chosen username is already in use. Please choose a different one.")

    # Validation successfully passed
    return True


def signin_validation(username, password, user_data):
    '''
    Checks for valid user input form in signin route.
    '''     
    # Ensure username was submitted
    if not username:
        raise ValueError('Username not entered')

    # Ensure password was submitted
    if not password:
        raise ValueError('Password not entered')
    
    # Ensure username exists and password is correct
    if not user_data or not check_password_hash(user_data[0]['hash'], password):
        raise ValueError('Wrong username or password')


def comma(integer):
    return f"{integer:,}"


def whitespace(text):
    return text.replace('_', ' ').title()


def get_list_of_values(json_data, column_name):
    '''
    Converts a json file into a list with values of
    the selected column
    '''
    return [item[column_name] for item in json_data]


def validate_submitted_digits(square_meters, rental, bedrooms, bathrooms):
    '''
    Checks if user has input valid digits in the digit-required fields or ranged fields
    '''
    must_be_numbers = [
        {
            "form_data": square_meters,
            "min": 0,
            "max": 1000,
            "field_name": "Square Meters"
        },
        {
            "form_data": rental,
            "min": 0,
            "max": 10000,
            "field_name": "Rental"
        },
        {
            "form_data": bedrooms,
            "min": 0,
            "max": 10,
            "field_name": "Bedrooms"
        },
        {
            "form_data": bathrooms,
            "min": 0,
            "max": 10,
            "field_name": "Bathrooms"
        },
    ]

    # Iterate through all must-be-numbers to validate them
    for number in must_be_numbers:
        form_data = number["form_data"]
        field_name = number["field_name"]

        # Ensure the digit value is not blank or None
        if not bool(form_data):
            raise ValueError(f'Invalid input for {field_name}. Please enter valid numbers.')

        # In case the request comes from sumbit.html or edit_submission.html the value should be a string
        elif isinstance(form_data, str):
            # Ensure the value is a digit
            if not form_data.isdigit():
                raise ValueError(f'Invalid input for {field_name}. Please enter a valid number.')

            # Validate the range of each number if its within proper range
            form_data = int(form_data)
            if form_data < number['min'] or form_data > number['max']:
                raise ValueError(f'Invalid {field_name}. Number must be between {number["min"]} and {number["max"]}.')
            
        else:
            raise ValueError(f'Invalid input type for {field_name}. Please enter a valid number or range.')

        
def check_submitted_location(submitted_value, valid_values, error_message):
    '''
    Checks if a user's submitted value is actually
    stored in the database
    '''
    if submitted_value not in valid_values:
        raise ValueError(error_message)
    

def validate_submitted_location(city, municipality, region):
    '''
    Regarding location data, this function checks if the select
    option values are actually valid by comparing them with the
    valid values that are stored in the database
    '''
    # Fetch location data from the database
    cities_json = cursor_fetch('SELECT DISTINCT city FROM cities')
    municipalities_json = cursor_fetch('SELECT DISTINCT municipality FROM municipalities')
    regions_json = cursor_fetch('SELECT DISTINCT region FROM regions')

    # Extract location values into lists
    cities = get_list_of_values(cities_json, 'city')
    municipalities = get_list_of_values(municipalities_json, 'municipality')
    regions = get_list_of_values(regions_json, 'region')

    # Validate submitted location values
    check_submitted_location(city, cities, "Invalid city value. Not found in the database")
    check_submitted_location(municipality, municipalities, "Invalid municipality value. Not found in the database")
    check_submitted_location(region, regions, "Invalid region value. Not found in the database")


def submission_validation(
        all_field_values,
        exposure,
        house_type,
        square_meters,
        rental,
        bedrooms,
        bathrooms,
        city,
        municipality,
        region,
    ):
    '''
    Checks for valid input form in submit/edited_submission routes.
    If any new input form will be available in the future add here
    conditionals for backend validation check
    '''

    # Ensure that all required fields are not blank
    if not all(field for field in all_field_values):
        raise ValueError('Some required fields weren\'t filled in.')

    # Declare a list of valid options for exposure value
    exposure_valid_options = [
        'public',
        'private',
    ]

    # Declare a list of valid options for house_type value
    house_type_options = [
        'studio',
        'flat',
        'maisonette',
        'semi-detached_house',
        'detached_house',
        'mansion',
    ]

    # Ensure exposure and house_type values are valid
    if (
        exposure not in exposure_valid_options or
        house_type not in house_type_options
    ):
        raise ValueError('Invalid exposure and/or house type.')

    # Ensure submitted digit-required values or value ranges are valid
    validate_submitted_digits(square_meters, rental, bedrooms, bathrooms)

    # Ensure submitted location values are valid
    validate_submitted_location(city, municipality, region)

    return True


def password_reset_validation(old_password, new_password, confirm_new_password, hash):
    '''
    Checks password reset input validity in account route.
    '''
    # Ensure fields are not blank
    if not old_password or not new_password or not confirm_new_password:
        raise ValueError("Please fill in all the required fields.")
    
    # Ensure old password is correct
    if not check_password_hash(hash[0]['hash'], old_password):
        raise ValueError('Wrong old password')

    # Ensure password and confirmation match
    if new_password != confirm_new_password:
        raise ValueError("New password and new password confirmation do not match.")

    # # Ensure password is strong
    if not is_strong_password(new_password):
        raise ValueError("Password must be at least 8 characters long, including at least 1 uppercase letter, 1 lowercase letter, a decimal number, and a punctuation character.")

    # Validation successfully passed
    return True


def update_username_validation(new_username, user_id):
    '''
    Checks password reset input validity in account route.
    '''
    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 20

    # Ensure field is not blank
    if not new_username:
        raise ValueError("Please fill in all the required field.")

    # Ensure new username does not exist
    if is_username_exists(new_username, user_id):
        raise ValueError("The chosen username is already in use. Please choose a different one.")
    
    # Ensure new username does not fall short the minimum length
    if len(new_username) < MIN_USERNAME_LENGTH:
        raise ValueError(f"Username must be at least {MIN_USERNAME_LENGTH} characters long.")
    
    # Ensure new username does not exceed the maximum length
    if len(new_username) > MAX_USERNAME_LENGTH:
        raise ValueError(f"Username cannot exceed {MAX_USERNAME_LENGTH} characters.")

    # Ensure new username does not contain punctuation characters or whitespaces
    if any(char in string.punctuation or char.isspace() for char in new_username):
        raise ValueError("Username cannot contain punctuation characters or whitespaces.")
    
    # Ensure new username is not the same as the previous one
    if session['username'] == new_username:
        raise NameError("Current username entered. Changes were not saved.")
    

def delete_account_validation(delete_account_confirmation, email):
    '''
    Checks password reset input validity in account route.
    '''
    # Ensure email has provided correctly to procceed to submissions and username deletion
    if delete_account_confirmation != email[0]['email']:
        raise ValueError("Wrong email. Account deletion aborted.")
    

def validate_searched_digits(square_meters, rental, bedrooms, bathrooms):
    '''
    Checks if user has input valid digits in the digit-required fields or ranged fields
    '''
    must_be_numbers = [
        {
            "form_data": square_meters,
            "min": 0,
            "max": 1000,
            "field_name": "Square Meters"
        },
        {
            "form_data": rental,
            "min": 0,
            "max": 10000,
            "field_name": "Rental"
        },
        {
            "form_data": bedrooms,
            "min": 0,
            "max": 10,
            "field_name": "Bedrooms"
        },
        {
            "form_data": bathrooms,
            "min": 0,
            "max": 10,
            "field_name": "Bathrooms"
        },
    ]

    # Iterate through all must-be-numbers to validate them
    for number in must_be_numbers:
        form_data = number["form_data"]
        field_name = number["field_name"]

        # Ensure the digit value is not blank or None
        if not bool(form_data):
            raise ValueError(f'Invalid input for {field_name}. Please enter valid numbers.')

        # In case the request comes from search.html the range values should be a dict
        if isinstance(form_data, dict):
            # Check if the values are digits
            if not isinstance(form_data['min'], int) or not isinstance(form_data['max'], int):
                raise ValueError (f'Invalid input for {field_name}. Please enter valid numbers.')

            # Validate the range of each number if its within proper range
            if form_data['min'] < number['min'] or form_data['min'] > number['max']:
                raise ValueError(f'Invalid {field_name}. Number must be between {number["min"]} and {number["max"]}.')
            
            if form_data['max'] < number['min'] or form_data['max'] > number['max']:
                raise ValueError(f'Invalid {field_name}. Number must be between {number["min"]} and {number["max"]}.')
                        
        else:
            raise ValueError(f'Invalid input type for {field_name}. Please enter a valid number or range.')

    
def validate_searched_location(city, municipality, region):
    '''
    Regarding location data, this function checks if the select
    option values are actually valid by comparing them with the
    valid values that are stored in the database
    '''
    # Fetch location data from the database
    cities_json = cursor_fetch('SELECT DISTINCT city FROM cities')
    municipalities_json = cursor_fetch('SELECT DISTINCT municipality FROM municipalities')
    regions_json = cursor_fetch('SELECT DISTINCT region FROM regions')

    # Extract location values into lists
    cities = get_list_of_values(cities_json, 'city')
    municipalities = get_list_of_values(municipalities_json, 'municipality')
    regions = get_list_of_values(regions_json, 'region')

    # In case the request is from search.html then set blank value as valid
    cities.append('')
    municipalities.append('')
    regions.append('')

    # Validate submitted location values
    check_submitted_location(city, cities, "Invalid city value. Not found in the database")
    check_submitted_location(municipality, municipalities, "Invalid municipality value. Not found in the database")
    check_submitted_location(region, regions, "Invalid region value. Not found in the database")


def search_validation(
        exposure,
        house_type,
        square_meters,
        rental,
        bedrooms,
        bathrooms,
        city,
        municipality,
        region,
    ):
    '''
    Checks for valid input form in submit/edited_submission routes.
    If any new input form will be available in the future add here
    conditionals for backend validation check
    '''

    # Declare a list of valid options for exposure value
    exposure_valid_options = [
        'public',
        'private',
        ''
    ]

    # Declare a list of valid options for house_type value
    house_type_options = [
        'studio',
        'flat',
        'maisonette',
        'semi-detached_house',
        'detached_house',
        'mansion',
        ''
    ]

    # Ensure exposure and house_type values are valid
    if (
        exposure not in exposure_valid_options or
        house_type not in house_type_options
    ):
        raise ValueError('Invalid exposure and/or house type.')

    # Ensure submitted digit-required values or value ranges are valid
    validate_searched_digits(square_meters, rental, bedrooms, bathrooms)

    # Ensure submitted location values are valid
    validate_searched_location(city, municipality, region)

    return True