import json
from fhelpers import cursor_execute
from fSQL import create_database_tables

create_database_tables()

with open('tdumsubmissions.json', 'r') as json_file:
    submissions = json.load(json_file)

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

    for submission in submissions:
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
