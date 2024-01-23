from fSQL import cursor_fetch
from fhelpers import get_list_of_values, check_submitted_location


def validate_searched_digits(square_meters, rental, bedrooms, bathrooms):
    '''
    Checks if user has input valid digits in the digit-required
    fields or ranged fields
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
            raise ValueError(
                f'Invalid input for {field_name}. Please enter valid numbers.'
            )

        # If request came from search.html, range values should be a dict
        if isinstance(form_data, dict):
            # Check if the values are digits
            if not isinstance(
                form_data['min'], int
            ) or not isinstance(
                form_data['max'], int
            ):
                raise ValueError(
                    f'Invalid input for {field_name}. Please enter valid numbers.'
                )

            # Check if range of each number is within proper range
            if (
                form_data['min'] < number['min']
            ) or (
                form_data['min'] > number['max']
            ):
                raise ValueError(
                    f'''
                    Invalid {field_name}. Number must be between {number["min"]}
                    and {number["max"]}.
                    '''
                )
            
            if (
                form_data['max'] < number['min']
            ) or (
                form_data['max'] > number['max']
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
                or range.
                '''
            )

    
def validate_searched_location(city, municipality, region):
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

    # In case the request is from search.html then set blank value as valid
    cities.append('')
    municipalities.append('')
    regions.append('')

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