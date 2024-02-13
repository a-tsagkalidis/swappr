from fSQL import cursor_fetch
from fhelpers import get_list_of_values, check_submitted_location

# Constant variables for inputs that require numbers
SQUARE_METERS_MIN = 30
SQUARE_METERS_MAX = 200
RENTAL_MIN = 100
RENTAL_MAX = 2000
BEDROOMS_MIN = 1
BEDROOMS_MAX = 4
BATHROOMS_MIN = 1
BATHROOMS_MAX = 2

# Constant variables for handling rooms-related tolerance factors
ROOMS_TOLERANCE_MIN = 30
ROOMS_TOLERANCE_MAX = 70
BEDROOMS_RTN_MIN = 0
BEDROOMS_RTN_MID = 1
BEDROOMS_RTN_MAX = 2
BATHROOMS_RTN_MIN = 0
BATHROOMS_RTN_MID = 0
BATHROOMS_RTN_MAX = 1


def room_tolerance_factor(tolerance, room):
    '''
    Regarding rooms, the function will return the tolerance factor that
    adjusts the maximum value of the CRITERIA_RANGES
    '''
    if room == 'bedrooms':
        if tolerance < ROOMS_TOLERANCE_MIN:
            return BEDROOMS_RTN_MIN
        elif tolerance < ROOMS_TOLERANCE_MAX:
            return BEDROOMS_RTN_MID
        else:
            return BEDROOMS_RTN_MAX
    elif room == 'bathrooms':
        if tolerance < ROOMS_TOLERANCE_MIN:
            return BATHROOMS_RTN_MIN
        elif tolerance < ROOMS_TOLERANCE_MAX:
            return BATHROOMS_RTN_MID
        else:
            return BATHROOMS_RTN_MAX
    else:
        return 0


def tolerance_factors(tolerance):
    '''
    Returns a dictionary of varied multipliers according to the user's
    selected amount of matching tolerance. These multipliers will be used
    to create the criteria ranges that they will eventually be used to
    calculate the house matching score for each searched house.

    The name of the dictionaty is declared with uppercase letters just
    to place it early in the code and access it easily if any adjustments
    should take place.
    '''
    TOLERANCE_FACTORS = {
        'square_meters': tolerance / 100,
        'rental': tolerance / 100,
        'bedrooms': room_tolerance_factor(tolerance, room='bedrooms'),
        'bathrooms': room_tolerance_factor(tolerance, room='bathrooms')
    }

    return TOLERANCE_FACTORS


def criteria_ranges(primary_submission, TOLERANCE_FACTORS):
    '''
    Returns a dictionary of varied ranges to be used in the calculation
    of the matching score for each search house result.

    The name of the dictionaty is declared with uppercase letters just
    to place it early in the code and access it easily if any adjustments
    should take place.
    '''
    CRITERIA_RANGES = {
        'square_meters':
        {
            'min': int(
                (
                    primary_submission[0]['square_meters']
                ) * (
                    1 - TOLERANCE_FACTORS['square_meters'] * .25
                )
            ),
            'max': int(
                (
                    primary_submission[0]['square_meters']
                ) * (
                    1 + TOLERANCE_FACTORS['square_meters']
                )
            )
        },
        'rental':
        {
            'min': 0,
            'max': int(
                (
                    primary_submission[0]['rental']
                ) * (
                    1 + TOLERANCE_FACTORS['rental']
                )
            )
        },
        'bedrooms':
        {
            'min': int(primary_submission[0]['bedrooms']),
            'max': int(
                (
                    primary_submission[0]['bedrooms']
                ) + (
                    TOLERANCE_FACTORS['bedrooms']
                )
            )
        },
        'bathrooms':
        {
            'min': int(primary_submission[0]['bathrooms']),
            'max': int(
                (
                    primary_submission[0]['bathrooms']
                ) + (
                    TOLERANCE_FACTORS['bathrooms']
                )
            )
        }
    }

    return CRITERIA_RANGES


def validate_searched_digits(
        square_meters,
        rental,
        bedrooms,
        bathrooms
    ):
    '''
    Validates digit-required and ranged-required input fields.
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

    
def validate_searched_location(
        city,
        municipality,
        region
    ):
    '''
    Regarding location data, this function checks if the select
    option values are actually valid by comparing them with the
    valid values that are stored in the database.
    '''
    # Fetch location data from the database
    query = '''
            SELECT DISTINCT city FROM cities;
            '''
    cities_json = cursor_fetch(query)
    query = '''
            SELECT DISTINCT municipality FROM municipalities;
            '''
    municipalities_json = cursor_fetch(query)
    query = '''
            SELECT DISTINCT region FROM regions
            '''
    regions_json = cursor_fetch(query)

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
        region
    ):
    '''
    Checks for valid input in search route form.
    
    If any new input form will be available in the future add here
    conditionals for backend validation check.
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


def calculate_location_matching_score(result, primary_submission):
    '''
    Returns a matching score regarding location. The function recieves as
    arguments one submission from the search results and the user's
    primary submission. It then compares the locations based on city,
    municipality, and region to increase or decrease the location mathing
    score accordingly.
    '''
    # Declare a score variable for location matching
    location_matching_score = 0

    # Check if desired city destination matches in search results
    # Αν η πόλη που ψάχνει ο user είναι ίδια με του result ή
    # αν ο user ψάχνει για οποιαδήποτε πόλη ή
    # τίποτα από τα 2
    if (
        primary_submission[0]['city_destination'] == result['city']
    ) or (
        primary_submission[0]['city_destination'] == 'any'
    ):
        if primary_submission[0]['city_destination'] == result['city']:
            location_matching_score += 2
        else:
            location_matching_score += 1
    else:
        location_matching_score -= 25

    # Αν η πόλη που ψάχνει το result είναι ίδια με του user ή
    # αν το result ψάχνει οποιαδήποτε πόλη ή
    # τίποτα από τα 2
    if (
        result['city_destination'] == primary_submission[0]['city']
    ) or (
        result['city_destination'] == 'any'
    ):
        if result['city_destination'] == primary_submission[0]['city']:
            location_matching_score += 2
        else:
            location_matching_score += 1
    else:
        location_matching_score -= 25

    # Check if desired municipality destination matches in search results
    # Αν ο νομός που ψάχνει ο user είναι ίδιος με του result ή
    # αν ο user ψάχνει για οποιοδήποτε νομό στην πόλη του user ή
    # τίποτα από τα 2
    if (
        primary_submission[0]['municipality_destination'] == result['municipality']
    ) or (
        (
            primary_submission[0]['municipality_destination'] == 'any'
        ) and (
            (
                primary_submission[0]['city_destination'] == result['city']
            ) or (
                primary_submission[0]['city_destination'] == 'any'
            ) 
        )
    ):
        if primary_submission[0]['municipality_destination'] == result['municipality']:
            location_matching_score += 4
        else:
            location_matching_score += 2
    else:
        location_matching_score -= 15

    # Αν ο νομός που ψάχνει το result είναι ίδιος με του user ή
    # αν το result ψάχνει για οποιοδήποτε νομό στην πόλη του user ή
    # τίποτα από τα 2
    if (
        result['municipality_destination'] == primary_submission[0]['municipality']
    ) or (
        (
            result['municipality_destination'] == 'any'
        ) and (
            (
                result['city_destination'] == primary_submission[0]['city']
            ) or (
                result['city_destination'] == 'any'
            )
        )
    ):
        if result['municipality_destination'] == primary_submission[0]['municipality']:
            location_matching_score += 4
        else:
            location_matching_score += 2
    else:
        location_matching_score -= 15

    # Check if desired region destination matches in search results
    # Αν η περιοχή που ψάχνει ο user είναι ίδια με του result ή
    # αν ο user ψάχνει για οποιαδήποτε περιοχή στην πόλη/νομό του user ή
    # τίποτα από τα 2
    if (
        primary_submission[0]['region_destination'] == result['region']
    ) or (
        (
            primary_submission[0]['region_destination'] == 'any'
        ) and (
            (
                primary_submission[0]['municipality_destination'] == result['municipality']
            ) or (
                (
                    primary_submission[0]['municipality_destination'] == 'any'
                ) and (
                    (
                        primary_submission[0]['city_destination'] == result['city']
                    ) or (
                        primary_submission[0]['city_destination'] == 'any'
                    ) 
                ) 
            )
        )
    ):
        if primary_submission[0]['region_destination'] == result['region']:
            location_matching_score += 6
        else:
            location_matching_score += 3
    else:
        location_matching_score -= 5

    # Αν η περιοχή που ψάχνει το result είναι ίδια με του user ή
    # αν το result ψάχνει για οποιαδήποτε περιοχή στην πόλη/νομό του user ή
    # τίποτα από τα 2
    if (
        result['region_destination'] == primary_submission[0]['region']
    ) or (
        (
            result['region_destination'] == 'any'
        ) and (
            (
                result['municipality_destination'] == primary_submission[0]['municipality']
            ) or (
                (
                    result['municipality_destination'] == 'any'
                ) and (
                    (
                        result['city_destination'] == primary_submission[0]['city']
                    ) or (
                        result['city_destination'] == 'any'
                    )
                )
            )
        )
    ):
        if result['region_destination'] == primary_submission[0]['region']:
            location_matching_score += 6
        else:
            location_matching_score += 3
    else:
        location_matching_score -= 5

    return location_matching_score


def location_matching(primary_submission, search_results):
    '''
    Iterates all search results and passes them into
    calculate_location_matching_score to compare them with the user's
    primary submission. Eventually the function adds a key/value pair
    into the searched result, that indicates the location matching score.
    '''
    for result in search_results:
        location_matching_score = calculate_location_matching_score(result, primary_submission)
        result['location_matching_score'] = location_matching_score


def calculate_house_matching_score(result, CRITERIA_RANGES):
    '''
    Returns a matching score regarding house characteristics. The
    function recieves as arguments one submission from the search results 
    and the user's primary submission. It then compares the house
    characteristics based on square_meters, rental, bedrooms, and
    bathrooms to increase or not the house matching score accordingly.
    '''
    # Declare a score variable for house matching
    house_matching_score = 0
    
    for criteria, ranges in CRITERIA_RANGES.items():
        if ranges['min'] <= result[criteria] <= ranges['max']:
            house_matching_score += 5
        else:
            house_matching_score -= 5

    return house_matching_score


def house_matching(search_results, CRITERIA_RANGES):
    '''
    Iterates all search results and passes them into
    calculate_house_matching_score to compare them with the user's
    primary submission.
    
    Each characteristic's value to be compared is stored in
    CRITERIA_RANGES with a min and max value that is shaped according
    to user's tolerance value from the form.
    
    Eventually the function adds a key/value pair
    into the searched result, that indicates the houses characteristics
    matching score.
    '''
    for result in search_results:        
        house_matching_score = calculate_house_matching_score(result, CRITERIA_RANGES)
        result['house_matching_score'] = house_matching_score


def matching_summary(search_results):
    '''
    Iterates all search results and adds all the matching scores to
    eventually create a new key/value pair into every searched result
    that indicates the total matching score.
    '''
    for result in search_results:
        result['total_matching_score'] = (result['location_matching_score'] + result['house_matching_score'])

