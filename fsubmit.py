import pprint as pp
from fhelpers import cursor_execute, cursor_fetch, get_list_of_values, check_submitted_location

# Constant variables for inputs that require numbers
SQUARE_METERS_MIN = 30
SQUARE_METERS_MAX = 200
RENTAL_MIN = 100
RENTAL_MAX = 2000
BEDROOMS_MIN = 1
BEDROOMS_MAX = 4
BATHROOMS_MIN = 1
BATHROOMS_MAX = 2


def validate_submitted_digits(square_meters, rental, bedrooms, bathrooms):
    '''
    Checks if user has input valid digits in the digit-required fields
    or ranged fields
    '''
    must_be_numbers = [
        {
            "form_data": square_meters,
            "min": SQUARE_METERS_MIN,
            "max": SQUARE_METERS_MAX,
            "field_name": "Square Meters"
        },
        {
            "form_data": rental,
            "min": RENTAL_MIN,
            "max": RENTAL_MAX,
            "field_name": "Rental"
        },
        {
            "form_data": bedrooms,
            "min": BEDROOMS_MIN,
            "max": BEDROOMS_MAX,
            "field_name": "Bedrooms"
        },
        {
            "form_data": bathrooms,
            "min": BATHROOMS_MIN,
            "max": BATHROOMS_MAX,
            "field_name": "Bathrooms"
        },
    ]

    # Iterate through all must-be-numbers to validate them
    for number in must_be_numbers:
        form_data = number['form_data']
        field_name = number['field_name']

        # Ensure the digit value is not blank or None
        if not bool(form_data):
            raise ValueError(
                f'Invalid input for {field_name}. Please enter valid numbers.'
            )

        # If request came from sumbit.html or edit_submission.html value should be a string
        elif isinstance(form_data, str):
            # Ensure the value is a digit
            if not form_data.isdigit():
                raise ValueError(
                    f'''
                    Invalid input for {field_name}. Please enter a valid number.
                    '''
                )

            # Validate the range of each number if its within proper range
            form_data = int(form_data)
            if (
                form_data < number['min']
            ) or (
                form_data > number['max']
            ):
                raise ValueError(
                    f'''
                    Invalid {field_name}. Number must be between {number["min"]}
                    and {number["max"]}.
                    '''
                )
            
        else:
            raise ValueError(
                f'''
                Invalid input type for {field_name}. Please enter a valid number
                or range.'''
            )


# def validate_submitted_location_or_destination(
#         city,
#         municipality,
#         region,
#         destination=False,
#     ):
#     '''
#     Regarding location data, this function checks if the select
#     option values are actually valid by comparing them with the
#     valid values that are stored in the database
#     '''
#     # Fetch location data from the database
#     cities_json = cursor_fetch(
#         'SELECT DISTINCT city FROM cities'
#     )
#     municipalities_json = cursor_fetch(
#         'SELECT DISTINCT municipality FROM municipalities'
#     )
#     regions_json = cursor_fetch(
#         'SELECT DISTINCT region FROM regions'
#     )

#     # Extract location values into lists
#     cities = get_list_of_values(cities_json, 'city')
#     municipalities = get_list_of_values(municipalities_json, 'municipality')
#     regions = get_list_of_values(regions_json, 'region')

#     if destination:
#         cities.append('any')
#         municipalities.append('any')
#         regions.append('any')

#     # Validate submitted location or destination values
#     check_submitted_location(
#         city,
#         cities,
#         'Invalid city value. Not found in the database'
#     )
#     check_submitted_location(
#         municipality,
#         municipalities,
#         'Invalid municipality value. Not found in the database'
#     )
#     check_submitted_location(
#         region,
#         regions,
#         'Invalid region value. Not found in the database'
#     )






def validate_submitted_location(
        city,
        municipality,
        region,
    ):
    '''
    Regarding location data, this function checks if the select
    option values are actually valid by comparing them with the
    valid values that are stored in the database
    '''
    # Fetch all valid cities from the database
    query = '''
            SELECT DISTINCT city FROM cities;
            '''
    cities_json = cursor_fetch(query)

    # Extract city values into lists
    cities = get_list_of_values(cities_json, 'city')

    if city == 'any':
        cities.append(city)

    # Validate submitted city location or destination value
    check_submitted_location(
        city,
        cities,
        'Invalid city value. Not found in the database'
    )

    # Fetch id of selected city to use it for valid municipality fetch
    if city in cities and city != 'any':
        query = '''
                SELECT id FROM cities
                WHERE city = ?;
                '''
        city_id = cursor_fetch(
            query,
            city
        )
        pp.pprint(cities)
        pp.pprint(city_id)
    elif city == 'any':
        pass
    else:
        raise ValueError('Invalid city value. Not found in the database')
    


    municipalities=[]
    if city in cities and city != 'any' and municipality != 'any':
        # Fetch all valid municipalities from the database
        query = '''
                SELECT DISTINCT municipality FROM municipalities
                WHERE city_id = ?;
                '''
        municipalities_json = cursor_fetch(
            query,
            city_id[0]['id']
        )

        # Extract municipality values into lists
        municipalities = get_list_of_values(municipalities_json, 'municipality')

        # Validate submitted municipality location or destination value
        check_submitted_location(
            municipality,
            municipalities,
            'Invalid municipality value. Not found in the database'
        )

        # Fetch id of selected municipality to use it for valid region fetch
        query = '''
                SELECT id FROM municipalities
                WHERE municipality = ?;
                '''
        municipality_id = cursor_fetch(
            query,
            municipality
        )
        pp.pprint(municipalities)
        pp.pprint(municipality_id[0]['id'])
    elif municipality == 'any':
        pass
    else:
        raise ValueError('Invalid municipality value. Not found in the database')

    
    regions=[]
    if (city in cities and city != 'any' and municipality in municipalities and municipality != 'any' and region != 'any'):
        # Fetch all valid regions from the database
        query = '''
                SELECT DISTINCT region FROM regions
                WHERE municipality_id = ?;
                '''
        regions_json = cursor_fetch(
            query,
            municipality_id[0]['id']
        )

        # Extract region values into lists
        regions = get_list_of_values(regions_json, 'region')

        # Append 'any' as valid region value if it's destination check
        if region == 'any':
            regions.append('any')

        # Validate submitted region location or destination value
        check_submitted_location(
            region,
            regions,
            'Invalid region value. Not found in the database'
        )
        pp.pprint(regions)
    elif region == 'any':
        pass
    else:
        raise ValueError('Invalid region value. Not found in the database')







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
        city_destination,
        municipality_destination,
        region_destination
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
    validate_submitted_digits(
        square_meters,
        rental,
        bedrooms,
        bathrooms
    )

    # Ensure submitted location values are valid
    validate_submitted_location(
        city,
        municipality,
        region
    )

    # Ensure submitted destination values are valid
    validate_submitted_location(
        city_destination,
        municipality_destination,
        region_destination
    )

    return True


def user_submissions_exist(user_id):
    '''
    Checks if the user has at least one submission in the database and
    after that it looks for user's primary submission. In case it finds
    the primary submission it returns True; otherwise False.

    This returned boolean will determine the primarySubmission checkbox
    in the html forms at @submit and @edited_submission routes
    '''
    # Select all the user's submissions
    query = '''
            SELECT * FROM submissions
            WHERE user_id = ?;
            '''
    user_submissions = cursor_fetch(
        query,
        user_id
    )
    
    # Check if the user has at least 1 submission
    if len(user_submissions) < 1:
        return False
    else:
        # Look for user's primary submission
        for submission in user_submissions:
            if submission['primary_submission'] == 1:
                return True
        return False


def determine_primary_submission_status(
        primary_submission,
        primary_submission_locked,
        user_id
    ):
    '''
    Determines the status of the primarySubmission checkbox in html
    forms at @submit and @edited_submission routes.

    Returns True (checked checkbox) in case the user has no submissions.

    Returns True in case the user saves an already primary submission or
    in case he sets a new submission or an edited submission as the new
    primary. In that case it also set all other submissions to
    non-primary statuses.

    Otherwise returns False (unchecked checkbox).
    '''
    # Check if the user has at least one submission that is primary
    if not user_submissions_exist(user_id):
        return True
    elif primary_submission_locked or primary_submission:
        # Set primary_submission status to False for all user's submissions
        query = '''
                UPDATE submissions SET
                    primary_submission = ?
                WHERE user_id = ?;
                '''
        cursor_execute(
            query,
            False,
            user_id
        )
        return True
    else:
        return False


def handle_primary_submission_upon_deletion(submission_id, user_id):
    '''
    Handles primary submission in database upon submission deletion.
    In case the submission to be deleted has non-primary status, the
    function returns False and the submission is deleted instantly
    (code in route).

    In case the submission to be deleted is of primary status but the
    user has also more than one submissions in the database, then the
    submission is deleted and the oldest submission is set as the new
    primary one. In that case the function returns True and the `if`
    conditional statement in the route gets passed.
    '''
    # Fetch primary submission status of submission to be deleted
    query = '''
            SELECT primary_submission FROM submissions
            WHERE id = ?
            AND user_id = ?;
            '''
    primary_submission_data = cursor_fetch(
        query,
        submission_id,
        user_id
    )

    # Fetch all the user's submissions
    query = '''
            SELECT * FROM submissions
            WHERE user_id = ?;
            '''
    user_submissions = cursor_fetch(
        query,
        user_id
    )

    # Check if submission to be deleted isn't sole and if is primary
    if (
        primary_submission_data[0]['primary_submission'] == 1
    ) and (
        len(user_submissions) > 1
    ):
        # Delete edited submission from database
        query = '''
                DELETE FROM submissions
                WHERE id = ?
                AND user_id = ?;
                '''
        cursor_execute(
            query,
            submission_id,
            user_id
        )

        # Refetch all the user's submissions from updated database
        query = '''
                SELECT * FROM submissions
                WHERE user_id = ?;
                '''
        user_submissions = cursor_fetch(
            query,
            user_id
        )

        # Set the oldest submission as primary
        query = '''
                UPDATE submissions SET
                    primary_submission = ?
                WHERE id = ?
                AND user_id = ?;
                '''
        cursor_execute(
            query,
            True,
            user_submissions[0]['id'],
            user_id
        )
        return True
    else:
        return False
    