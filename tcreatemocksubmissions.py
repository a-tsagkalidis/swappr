import json
import subprocess
from tqdm import tqdm
from argparser import argparser
from random import choice, randint
from fSQL import create_database_tables
from fictional_names import name_generator
from fhelpers import cursor_execute, cursor_fetch


def round_rental(number):
    '''
    Rounds rental to the closest decade
    '''
    return round(number, -1)


def generate_user(id_increment, existing_names):
    '''
    Returns a dictionary of a randomly generated user. Duplicated names
    are prevented thanks to a set of existing_names that is imported
    as an argument. In case a name exists, then a suffix increment number
    is added to the name string for uniqueness.
    '''
    names = name_generator.generate_name

    while True:
        # Create a name for the mockup user entry
        name = names(
            gender=choice(['male', 'female']),
            style='english',
            library=False
        ).replace(" ", ".").lower()
        
        # Check if the generated name is unique
        if name not in existing_names:
            existing_names.add(name)
            break
        else:
            # Append a unique suffix to the name
            suffix = 1970 + randint(0, 36)
            new_name = f"{name}{suffix}"
            while new_name in existing_names:
                suffix += 1
                new_name = f"{name}{suffix}"
                
            name = new_name
            existing_names.add(name)
            break
    
    return {
        'user_id': id_increment + 1,
        'username': name.replace('.', ''),
        'email': f"{name}@swappr.com"
    }


def create_mockups(*args):
    '''
    This function creates two JSON files of generated mockup users and
    submissions respectively.
    
    The number of the generated mockups depends on the passed integer
    arguments that where given when app.py was ran with [-m int int]*.
    
    *check argparser.py
    '''
    # Asign argparser tuple arguments to int variables - tuples are immutable
    mockup_users = args[0]
    mockup_submissions = args[1]

    # Ensure that given mockup submissions are less or equal to mockup users
    if mockup_submissions > mockup_users:
        mockup_submissions = mockup_users

    # A list of valid house types, square meters, bedrooms, bathrooms,
    # exposure, and primary submission statuses to be declared in the mockup
    # submission entry
    house_type = [
        'studio',
        'flat',
        'maisonette',
        'semi-detached_house',
        'detached_house',
        'mansion'
    ]
    square_meters = [i for i in range(40, 120)]
    rental = [ i for i in range(300, 900)]
    bedrooms = [i for i in range(1, 4)]
    bathrooms = [i for i in range(1, 2)]
    exposure = 'public'
    primary_submission = 1

    # Create a list that will store the generated mockup user entries; In the
    # list is prestored by default the `admin` user for testing purposes
    generated_users = [
        {
            'user_id': 1,
            'username': 'admin',
            'email': 'admin@swappr.com'
        }
    ]

    # Declare a set where generated names are stored to prevent duplicates
    generated_names = set()

    # Append the generated mockup user entries in the users list
    for id in range(1, mockup_users):
        generated_user = generate_user(id, generated_names)
        generated_users.append(generated_user)

    # Convert and store the mockup users list into a JSON file
    json_data = json.dumps(generated_users, indent=4)
    with open('tmockusers.json', 'w') as f:
        f.write(json_data)

    # Data structure of all the valid locations; data from `locations.json`
    with open('locations.json') as f:
        locations = json.load(f)

    # Declare an empty list where the generated submissions will be stored
    generated_submissions = []

    # Declare an empty set where the users that already submitted a house will be stored
    used_users = set()

    # Create generated submissions equals requested times
    for i in range(mockup_submissions):
        # Create dictionaries to map cities to their corresponding municipalities
        # and regions for both source and destination
        random_location = choice(locations)
        random_destination = choice(locations)

        city_mapping_source = {
            random_location['city']: {
                random_location['municipality']: random_location['region']
            }
        }
        city_mapping_destination = {
            random_destination['city']: {
                random_destination['municipality']: random_destination['region']
            }
        }

        # Generate valid location data for source
        city_source = choice(list(city_mapping_source.keys()))
        municipality_region_mapping_source = city_mapping_source[city_source]
        municipality_source = choice(list(municipality_region_mapping_source.keys()))
        region_mapping_source = municipality_region_mapping_source[municipality_source]
        region_source = choice(list(region_mapping_source.keys()))
        postal_code_source = region_mapping_source[region_source]

        # Generate valid location data for destination
        city_destination = choice(
            list(
                city_mapping_destination.keys()
            )
        )
        municipality_region_mapping_destination = city_mapping_destination[city_destination]
        municipality_destination = choice(
            list(
                municipality_region_mapping_destination.keys()
            )
        )
        region_mapping_destination = municipality_region_mapping_destination[municipality_destination]
        region_destination = choice(
            list(
                region_mapping_destination.keys()
            )
        )
        
        # Select a random user who will own the generated submission
        random_user = choice(generated_users)
        # Prevent the user from owning more than one submission
        while True:
            if random_user['username'] not in used_users:
                used_users.add(random_user['username'])
                break
            else:
                random_user = choice(generated_users)

        # Generate mockup submission entry and store it in generated submissions list
        entry = {
            "bathrooms": choice(bathrooms),
            "bedrooms": choice(bedrooms),
            "city": city_source,
            "city_destination": city_destination,
            "email": random_user['email'],
            "exposure": exposure,
            "house_type": choice(house_type),
            "id": i + 1,
            "municipality": municipality_source,
            "municipality_destination": municipality_destination,
            "postal_code": postal_code_source,
            "primary_submission": primary_submission,
            "region": region_source,
            "region_destination": region_destination,
            "rental": round_rental(choice(rental)),
            "square_meters": choice(square_meters),
            "user_id": random_user['user_id'],
            "username": random_user['username']
        }
        generated_submissions.append(entry)

    # Convert and store the mockup users list into a JSON file
    json_data = json.dumps(generated_submissions, indent=4)
    with open('tmocksubmissions.json', 'w') as f:
        f.write(json_data)


def load_mockup_users(mockup_users):
    '''
    Opens the JSON file of generated mockup users, converts it into a
    dictionary and then passes the data into the database. By default
    the password is hashed for all users - login password is "1" for
    testing purposes.

    Before that, create_database_tables() function is called to check if
    the database is present; if not it creates it.
    '''
    with open(f'{mockup_users}', 'r') as f:
        users = json.load(f)

    query = '''
            INSERT INTO users (
                id,
                username,
                email,
                hash,
                registration_date,
                verified_account
            )
            VALUES (?, ?, ?, ?, ?, ?);
            '''

    for user in tqdm(users):
        cursor_execute(
            query,
            user['user_id'],
            user['username'],
            user['email'],
            'scrypt:32768:8:1$qICfKjC9CagbVSrn$efd605af1c704a9ba1ac242acad6e8a49d7568d60aa9028e54271d94a69ecc0ebfa75a56c9278a48db227e1b685337bba53c1170a5b6016ba7336083a8bd259c',
            '2024-02-03 09:38:41.231061',
            0
        )


def load_mockup_submissions(mockup_submissions):
    '''
    Opens the JSON file of generated mockup submissions, converts it
    into a dictionary and then passes the data into the database.

    Before that, create_database_tables() function is called to check if
    the database is present; if not it creates it.
    '''
    with open(f'{mockup_submissions}', 'r') as f:
        submissions = json.load(f)

    query = '''
            INSERT INTO submissions (
                user_id,
                house_type,
                square_meters,
                rental,
                bedrooms,
                bathrooms,
                city,
                municipality,
                region,
                city_destination,
                municipality_destination,
                region_destination,
                exposure,
                primary_submission
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            '''

    for submission in tqdm(submissions):
        cursor_execute(
            query,
            submission['user_id'],
            submission['house_type'],
            submission['square_meters'],
            submission['rental'],
            submission['bedrooms'],
            submission['bathrooms'],
            submission['city'],
            submission['municipality'],
            submission['region'],
            submission['city_destination'],
            submission['municipality_destination'],
            submission['region_destination'],
            submission['exposure'],
            submission['primary_submission']
        )


def insert_mockups(*args):
    '''
    Runs tload_mockusers.py and tload_mocksubmissions.py for testing
    purposes, after it wipes out the database and recreates it.
    
    The scripts are loading mockups that are stored in tmockusers.json 
    and tmocksubmisssions.json or tmockusers.json.bak and 
    tmocksubmisssions.json.bak in case of --mockupsgen or --premademockups
    given argument respectively.
    '''
    subprocess.run(['rm', '-rf', 'swappr.db'])
    create_database_tables()

    if argparser.mockupsgen and not argparser.premademockups:
        create_mockups(*args)
        mockup_users = 'tmockusers.json'
        mockup_submissions = 'tmocksubmissions.json'
    else:
        mockup_users = 'bak.json/tmockusers.json.bak'
        mockup_submissions = 'bak.json/tmocksubmissionsthess.json.bak'
    load_mockup_users(mockup_users)
    load_mockup_submissions(mockup_submissions)

    subprocess.run(['rm', '-rf', 'tmockusers.json'])
    subprocess.run(['rm', '-rf', 'tmocksubmissions.json'])
