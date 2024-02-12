import json
import sqlite3
from fhelpers import cursor_execute, cursor_fetch


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
            city_destination TEXT NOT NULL,
            municipality_destination TEXT NOT NULL,
            region_destination TEXT NOT NULL,
            exposure TEXT NOT NULL,
            primary_submission BOOLEAN NOT NULL,
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
    locations_update = {
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
        existing_city = cursor.execute(
            'SELECT id FROM cities WHERE city = ?',
            (city,)
        ).fetchone()

        if not existing_city:
            locations_update['cities'].append(city)
            locations_update['cities count'] += 1
            locations_update['total new entries'] += 1
            cursor.execute(
                'INSERT INTO cities (city) VALUES (?)',
                (city,)
            )
    
    # Commit the changes to ensure city IDs are available for foreign key references
    conn.commit()

    # Insert data into the 'municipalities' table
    for location in locations:
        city_id = cursor.execute(
            'SELECT id FROM cities WHERE city = ?',
            (location['city'],)
        ).fetchone()[0]
        municipality = location['municipality']
        
        # Check if the municipality already exists in the table
        existing_municipality = cursor.execute(
            'SELECT id FROM municipalities WHERE municipality = ?',
            (municipality,)
        ).fetchone()

        if not existing_municipality:
            locations_update['municipalities'].append(municipality)
            locations_update['municipalities count'] += 1
            locations_update['total new entries'] += 1
            cursor.execute(
                '''
                INSERT INTO municipalities (municipality, city_id) VALUES (?, ?)
                ''',
                (
                    municipality,
                    city_id
                )
            )

    # Commit the changes to ensure municipality IDs are available for foreign key references
    conn.commit()

    # Insert data into the 'regions' table
    for location in locations:
        municipality_id = cursor.execute(
            'SELECT id FROM municipalities WHERE municipality = ?',
            (location['municipality'],)
        ).fetchone()[0]

        # Check if the region already exists in the table
        for region, postal_code in location['region'].items():
            existing_region = cursor.execute(
                'SELECT id FROM regions WHERE region = ?',
                (region,)
            ).fetchone()

            if not existing_region:
                locations_update['regions'].append(region)
                locations_update['regions count'] += 1
                locations_update['total new entries'] += 1
                cursor.execute(
                    '''
                    INSERT INTO regions (region, postal_code, municipality_id) VALUES (?, ?, ?)
                    ''',
                    (
                        region,
                        postal_code,
                        municipality_id
                    )
                )

    # Commit the final changes and close the connection
    conn.commit()
    conn.close()

    new_locations_flag = False
    if (
        locations_update['cities']
    ) and (
        locations_update['municipalities']
    ) and (
        locations_update['regions']
    ):
        new_locations_flag = True

    return locations_update, new_locations_flag
