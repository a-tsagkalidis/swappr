from fhelpers import cursor_execute, cursor_fetch, get_list_of_values, check_submitted_location


def validate_submitted_digits(square_meters, rental, bedrooms, bathrooms):
    '''
    Checks if user has input valid digits in the digit-required fields
    or ranged fields
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


def validate_submitted_location(city, municipality, region):
    '''
    Regarding location data, this function checks if the select
    option values are actually valid by comparing them with the
    valid values that are stored in the database
    '''
    # Fetch location data from the database
    cities_json = cursor_fetch(
        'SELECT DISTINCT city FROM cities'
    )
    municipalities_json = cursor_fetch(
        'SELECT DISTINCT municipality FROM municipalities'
    )
    regions_json = cursor_fetch(
        'SELECT DISTINCT region FROM regions'
    )

    # Extract location values into lists
    cities = get_list_of_values(cities_json, 'city')
    municipalities = get_list_of_values(municipalities_json, 'municipality')
    regions = get_list_of_values(regions_json, 'region')

    # Validate submitted location values
    check_submitted_location(
        city,
        cities,
        'Invalid city value. Not found in the database'
    )
    check_submitted_location(
        municipality,
        municipalities,
        'Invalid municipality value. Not found in the database'
    )
    check_submitted_location(
        region,
        regions,
        'Invalid region value. Not found in the database'
    )


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



def user_submissions_exist(user_id):
    query = '''
            SELECT * FROM submissions
            WHERE user_id = ?;
            '''
    user_submissions = cursor_fetch(
        query,
        user_id
    )
    
    if len(user_submissions) < 1:
        return False
    else:
        for submission in user_submissions:
            if submission['primary_submission'] == 1:
                yield True
            else:
                yield False


def determine_primary_submission_status(primary_submission, user_id):
    if not user_submissions_exist(user_id):
        return True
    elif primary_submission:
        # Reset primary_submission for all submission into
        query = '''
                UPDATE submissions
                SET primary_submission = ?
                AND user_id = ?
                '''
        cursor_execute(
            query,
            False,
            user_id
        )
        return True
    else:
        return False