import os
import sys
import json
import secrets
import subprocess
from loguru import logger
from argparser import args
from swapprfunctions import *
from datetime import datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash
from flask import Flask, render_template, request, session, redirect, url_for, flash

import pprint
pp = pprint.PrettyPrinter(indent=4)

# Configure loguru
try:
    logger.remove(0)
    initialize_logger()
except Exception as err:
    print(f'Unexpected {err=}, {type(err)=}')
    raise

# Initialize basic functionalities
try:
    # Declare global variables for POST request limits
    SIGNUP_LIMIT = "60/minute"
    SIGNIN_LIMIT = "60/minute"
    SUBMIT_LIMIT = "30/minute"
    UPDATE_EXPOSURE_LIMIT = "30/minute"
    EDIT_SUBMISSION_LIMIT = "60/minute"
    SEARCH_LIMIT = "100/minute"
    PASSWORD_RESET_LIMIT = "30/minute"
    UPDATE_USERNAME_LIMIT = "30/minute"
    DELETE_ACCOUNT_LIMIT = "30/minute"

    # Declare global variable for datetime log format
    DATETIME = datetime.now().strftime(f"[%d/%b/%Y %H:%M:%S]")

    # Flask instance to initialize the web application.
    app = Flask(__name__)

    # Flask limiter instance for spam request protection
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["2000 per day", "500 per hour"],
        storage_uri="memory://",
    )

    # Run system file backup script - back ups database and logs
    if args.backup:
        logger.remove()
        os.system('bash fbak.sh')
        initialize_logger()

    # Obfuscate script.js into script.min.js
    if args.obfuscate:
        subprocess.run(
            [
                "powershell",
                "node_modules/.bin/uglifyjs.ps1",
                "static/js/script.js",
                '-o',
                'static/js/script.min.js',
                '-m',
                '-c',
            ],
                shell=True
            )

    # JSON instance to be used in log function for better readability
    dumps = json.dumps

    # Declare a secret key for Flask application - it is needed for flash function
    app.secret_key = secrets.token_hex(32)

    # Initialize the database and tables
    create_database_tables()

    # Import location data from locations.json file into proper database tables
    location_update, flag = import_locations()

    # In case of newly imported locations in the database inform properly the log
    if flag:
        # Updage log with WARNING msg
        log(
            f'''
            App initialized successfully. Database tables where created
            in case they weren't exist. JSON file with locations has been
            imported to the database - NEWLY IMPORTED LOCATIONS: 
            {dumps(location_update, indent=8)}
            ''',
            level='WARNING',
            indent=24
        )
    else:
        # Updage log with INFO msg
        log(
            f'''
            App initialized successfully. Database tables where created
            in case they weren't exist. JSON file with locations has been
            imported to the database - NO NEWLY IMPORTED LOCATIONS FOUND.
            ''',
            indent=24
        )

except Exception as err:
    log(f'Unexpected {err=}, {type(err)=}')
    raise


# ||||| ----- FLASK ROUTES ----- |||||

# |----- INDEX HTML ROUTE ----|
@app.route('/')
@login_required
def index():
    # Get user data
    user_id = session['user_id']

    # Fetch all submissions for the logged user
    query = '''
            SELECT * FROM submissions
            WHERE user_id = ?;
            '''
    submissions_data = cursor_fetch(query, user_id)
    
    # Update log with INFO msg
    log(
        f'''
        {session['ip']}
        USER[{session['username']}]: NAVIGATION: @index.html
        '''
    )
    return render_template(
        'index.html',
        submissions=submissions_data,
        comma=comma,
        whitespace=whitespace
    )


# |----- SIGN IN HTML AND POST BUTTON ROUTE ----|
@app.route('/signup', methods=['GET', 'POST'])
@limiter.limit(f"{SIGNUP_LIMIT}" if args.limiter else None)
def signup():
    if request.method == 'POST':
        # Get user submitted form data
        email = request.form.get('email').lower()
        username = request.form.get('username').lower()
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')

        # Check if all form fields are filled and valid
        try:
            # Ensure user form input for signup is valid
            signup_validation(
                email,
                username,
                password,
                confirm_password
            )

            # Hash password before storing it
            hashed_password = generate_password_hash(
                password,
                method='scrypt',
                salt_length=16
            )

            registration_date = datetime.now()

            # Sign up new user
            query = '''
                    INSERT INTO users (
                        email,
                        username,
                        hash,
                        registration_date,
                        verified_account
                    )
                    VALUES (?, ?, ?, ?, ?);
                    '''
            cursor_execute(
                query,
                email,
                username,
                hashed_password,
                registration_date,
                False
            )

            # Update log with INFO msg
            log(
                f'''
                {request.remote_addr}
                SUCCESS: New user 'registered'
                'email': {email}
                'username': {username}
                ''',
                indent=20
            )

            # Sign in new user
            signin()

            # Inform user for successful register
            message = {
                'success': 'Successfully registered!'
            }
            flash(message)
            return redirect(url_for('delayed_redirect'))

        except ValueError as err:
            # Update log with ERROR msg
            log(
                f'''
                [{request.remote_addr}]
                USER[unregistered]: FAILED: Sign up: {err}
                ''',
                level='WARNING',
                indent=24
            )
            
            return render_template('/signup.html', error=err)

    # Update log with INFO msg
    log(
        f'''
        {request.remote_addr}
        USER[unregistered]: NAVIGATION: @signup.html
        '''
    )

    return render_template('/signup.html')


# |----- DELAYED REDIRECT HTML ROUTE ----|
@app.route('/delayed_redirect')
def delayed_redirect():
    registration_timestamp = session.get('registration_timestamp')

    # Check if the registration timestamp is set
    if registration_timestamp:

        # Calculate the time elapsed since registration
        elapsed_time = datetime.now() - registration_timestamp

        # If more than 4 seconds have passed, redirect to the home page
        if elapsed_time >= 4:
            return redirect('/')

    # Update log with INFO msg
    log(
        f'''
        {session['ip']}
        USER[{session['username']}]: Redirection @index.html
        '''
        )

    # Render the delayed redirect template with a JavaScript redirect
    return render_template('delayed_redirect.html')


# |----- SIGNIN HTML AND POST BUTTON ROUTE ----|
@app.route("/signin", methods=['GET', 'POST'])
@limiter.limit(f"{SIGNIN_LIMIT}" if args.limiter else None)
def signin():
    # Forget any user_id
    session.clear()

    if request.method == 'POST':
        # Get user submitted form data
        username = request.form.get('username').lower()
        password = request.form.get('password')

        # Fetch user registered data
        query = '''
                SELECT * FROM users
                WHERE username = ?;
                '''
        user_data = cursor_fetch(query, username)

        # Check if all form fields are filled and valid
        try:
            # Ensure user form input for signin is valid
            signin_validation(
                username,
                password,
                user_data
            )

            # Store in session dictionary user details to be used later
            session['user_id'] = user_data[0]['id']
            session['username'] = user_data[0]['username']
            session['email'] = user_data[0]['email']
            session['ip'] = request.remote_addr
            session['logged_user'] = {
                'user_id': session['user_id'],
                'email': session['email'],
                'username': session['username'],
            }

            # Update log with INFO msg
            log(
                f'''
                {session['ip']}
                USER[{session['username']}]: Signed in
                ''',
                indent=20
            )

            # Redirect user to home page
            return redirect('/')

        except ValueError as err:
            # Update log with ERROR msg
            log(
                f'''
                {request.remote_addr}
                USER[{'unregistered'}]: FAILED: Signin: {err}
                ''',
                indent=20
            )

            return render_template('/signin.html', error=err)

    # Update log with INFO msg
    log(
        f'''
        {request.remote_addr}
        USER[unregistered]: NAVIGATION: @signin.html
        '''
    )
    return render_template('/signin.html')


# |----- SIGNOUT ROUTE ----|
@app.route('/signout')
@login_required
def signout():
    # Update log with INFO msg
    log(
        f'''
        {session['ip']}
        USER[{session['username']}]: Signed out
        '''
    )

    # Forget any user_id
    session.clear()
    return redirect('/')


# |----- SUBMIT HTML AND POST BUTTON ROUTE ----|
@app.route('/submit', methods=['GET', 'POST'])
@limiter.limit(f"{SUBMIT_LIMIT}" if args.limiter else None)
@login_required
def submit():
    # Fetch cities for the initial rendering of the form
    cities = cursor_fetch('SELECT DISTINCT city FROM cities')

    # Get user data
    user_id = session['user_id']

    if request.method == 'POST':
        # Get user submitted form data
        exposure = request.form.get('exposure')
        house_type = request.form.get('houseType')
        square_meters = request.form.get('squareMeters')
        rental = request.form.get('rental')
        bedrooms = request.form.get('bedrooms')
        bathrooms = request.form.get('bathrooms')
        city = request.form.get('city')
        municipality = request.form.get('municipality')
        region = request.form.get('region')
        city_destination = request.form.get('cityDestination')
        municipality_destination = request.form.get('municipalityDestination')
        region_destination = request.form.get('regionDestination')
        all_field_values = list(request.form.values())

        # Check if all form fields are filled and valid
        try:
            # Ensure user form input for submission is valid
            submission_validation(
                all_field_values,
                exposure,
                house_type,
                square_meters,
                rental,
                bedrooms,
                bathrooms,
                city,
                municipality,
                region
                #TODO add destination location details for validation
            )

            # Update log with WARNING msg
            log(
                f'''
                {session['ip']}
                USER[{session['username']}]: SUCCESS: Submission 'validated'
                ''',
                level='SUCCESS',
                indent=20
            )

            # Save submission into user database
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
                        exposure
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    '''
            cursor_execute(
                query,
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
                exposure
            )

            # Update log with INFO msg
            log(
                f'''
                {session['ip']}
                USER[{session['username']}]: SUCCESS: Submission 'saved'
                ''',
                level='SUCCESS',
                indent=20
            )

            # Inform user for successful submission
            message = {
                'success': 'Submission saved successfully!'
            }
            flash(message)
            return redirect('/')

        except ValueError as err:
            # Update log with ERROR msg
            log(
                f'''
                {session['ip']}
                USER[{session['username']}]: FAILED: Submission 'aborted': {err}
                ''',
                level='WARNING',
                indent=20
            )

            return render_template(
                '/submit.html',
                submission=None,
                error=err
            )

    else:
        # Update log with INFO msg
        log(
            f'''
            {session['ip']}
            USER[{session['username']}]: NAVIGATION: @submit.html
            ''',
            indent=24
        )

        return render_template(
            '/submit.html',
            cities=cities,
            submission=None,
            whitespace=whitespace
        )


# |----- UPDATE EXPOSURE POST BUTTON ROUTE ----|
@app.route('/update_exposure', methods=['POST'])
@limiter.limit(f"{UPDATE_EXPOSURE_LIMIT}" if args.limiter else None)
@login_required
def update_exposure():
    # Get user data
    user_id = session['user_id']

    # Retrieve data from the form
    submission_id = request.form.get('submission_id')
    new_exposure = request.form.get('new_exposure')

    # Update exposure value in the database
    query = '''
            UPDATE submissions
            SET exposure = ?
            WHERE id = ?
            AND user_id = ?;
            '''
    cursor_execute(
        query,
        new_exposure,
        submission_id,
        user_id
    )

    # Update log with INFO msg
    log(
        f'''
        {session['ip']}
        USER[{session['username']}]: SUCCESS: Submission id {submission_id} changed exposure -> '{new_exposure}'
        '''
    )

    # Inform user for successful exposure update
    message = {
        'success': 'Exposure updated successfully!'
    }
    flash(message)
    return redirect(url_for('index'))


# |----- EDIT SUBMISSION HTML AND POST BUTTON ROUTE ----|
@app.route('/edit_submission', methods=['POST'])
@limiter.limit(f"{EDIT_SUBMISSION_LIMIT}" if args.limiter else None)
@login_required
def edit_submission():
    # Fetch cities for the initial rendering of the form
    cities = cursor_fetch('SELECT DISTINCT city FROM cities')

    # Get user data
    user_id = session['user_id']

    # Retrieve data from the form
    submission_id = request.form.get('submission_id')

    try:
        # Ensure submission existance
        query = '''
                SELECT * FROM submissions
                WHERE id = ?
                AND user_id = ?;
                '''
        submission_data = cursor_fetch(query, submission_id, user_id)

        # If submission exists pass its data to the edit page, else reload index route
        if submission_data:
            # Update log with INFO msg
            log(
                f'''
                {session['ip']}
                USER[{session['username']}]: NAVIGATION: @edit_submission.html
                USER[{session['username']}]: SUCCESS: Submission id {submission_id} 'edit'
                ''',
                indent=20
            )

            return render_template(
                '/edit_submission.html',
                cities=cities,
                submission=submission_data[0],
                whitespace=whitespace,
            )
        
    except Exception as err:
        # Update log with ERROR msg
        log(
            f'''
            {session['ip']}
            USER[{session['username']}]: FAILED: Submission id {submission_id} 'not found': {err}
            ''',
            level='WARNING',
            indent=24
        )
        
        # Inform user for submission search error
        message = {
            'error': 'Submission not found.'
        }
        flash(message)
        return redirect(url_for('index'))


# |----- EDITED SUBMISSION SAVE AND DELETE POST BUTTON ROUTE ----|
@app.route('/edited_submission', methods=['POST'])
@limiter.limit(f"{EDIT_SUBMISSION_LIMIT}" if args.limiter else None)
@login_required
def save_edit_submission():
    # Fetch cities for the initial rendering of the form
    cities = cursor_fetch('SELECT DISTINCT city FROM cities')

    # Get user data
    user_id = session['user_id']

    # Retrieve data from the form
    submission_id = request.form.get('submission_id')
    house_type = request.form.get('houseType')
    square_meters = request.form.get('squareMeters')
    rental = request.form.get('rental')
    bedrooms = request.form.get('bedrooms')
    bathrooms = request.form.get('bathrooms')
    exposure = request.form.get('exposure')
    city = request.form.get('city')
    municipality = request.form.get('municipality')
    region = request.form.get('region')
    city_destination = request.form.get('cityDestination')
    municipality_destination = request.form.get('municipalityDestination')
    region_destination = request.form.get('regionDestination')
    all_field_values = list(request.form.values())

    # Save edited house or delete it
    if 'save' in request.form:
        # Check if all form fields are filled and valid
        try:
            # Ensure user form input for edit submission is valid
            submission_validation(
                all_field_values,
                exposure,
                house_type,
                square_meters,
                rental,
                bedrooms,
                bathrooms,
                city,
                municipality,
                region
                #TODO add destination location details for validation
            )
            # Update log with WARNING msg
            log(
                f'''
                {session['ip']}
                USER[{session['username']}]: SUCCESS: Edited submission {submission_id} 'validated'
                ''',
                level='WARNING',
                indent=20
            )

            # Update edited submission into user database
            query = '''
                    UPDATE submissions SET
                        house_type = ?,
                        square_meters = ?,
                        rental = ?,
                        bedrooms = ?,
                        bathrooms = ?,
                        city = ?,
                        municipality = ?,
                        region = ?,
                        city_destination = ?,
                        municipality_destination = ?,
                        region_destination = ?,
                        exposure = ?
                    WHERE id = ?
                    AND user_id = ?;
                    '''
            cursor_execute(
                query,
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
                submission_id,
                user_id
            )

            # Update log with INFO msg
            log(
                f'''
                {session['ip']}
                USER[{session['username']}]: SUCCESS: Sumbission {submission_id} 'updated'
                ''',
                indent=20
            )

            # Inform user for successful submission update
            message = {
                'success': 'Submission updated successfully!'
            }
            flash(message)
            return redirect(url_for('index'))

        except ValueError as err:
            # Update log with ERROR msg
            log(
                f'''
                {session['ip']}
                USER[{session['username']}]: FAILED: Submission update 'aborted': {err}
                ''',
                level='WARNING',
                indent=20
            )

            # Fetch edited submission data to reload route with correct field values
            query = '''
                    SELECT * FROM submissions
                    WHERE id = ?
                    AND user_id = ?;
                    '''
            submission_data = cursor_fetch(query, submission_id, user_id)
            return render_template(
                '/edit_submission.html',
                cities=cities,
                submission=submission_data[0],
                error=err,
                whitespace=whitespace,
            )
        
    if 'delete' in request.form:
        # Delete edited submission from database
        query = '''
                DELETE FROM submissions
                WHERE id = ?
                AND user_id = ?;
                '''
        cursor_execute(query, submission_id, user_id)

        # Update log with INFO msg
        log(
            f'''
            {session['ip']}
            USER[{session['username']}]: SUCCESS: Submission {submission_id} 'deleted'
            ''',
            indent=24
        )

        # Inform user for successful submission deletion
        message = {
            'success': 'Submission deleted successfully!'
        }
        flash(message)
        return redirect(url_for('index'))


# |----- GET MUNICIPALITIES SELECT INPUT ROUTE ----|
@app.route('/get_municipalities')
def get_municipalities():
    city = request.args.get('city')
    query = '''
            SELECT id FROM cities
            WHERE city = ?;
            '''
    city_data = cursor_fetch(query, city)
    city_id = city_data[0]['id']

    # Fetch municipalities from the database based on the selected city
    query = '''
            SELECT municipality FROM municipalities
            WHERE city_id = ?;
            '''
    municipalities = cursor_fetch(query, city_id)
    return municipalities


# |----- GET REGIONS SELECT INPUT ROUTE ----|
@app.route('/get_regions')
def get_regions():
    municipality = request.args.get('municipality')
    query = '''
            SELECT id FROM municipalities
            WHERE municipality = ?;
            '''
    municipality_data = cursor_fetch(query, municipality)
    municipality_id = municipality_data[0]['id']

    # Fetch regions from database based on selected city and municipality
    query = '''
            SELECT region FROM regions
            WHERE municipality_id = ?;
            '''
    regions = cursor_fetch(query, municipality_id)
    return regions


# |----- SEARCH HTML ROUTE ----|
@app.route('/search', methods=['GET', 'POST'])
@limiter.limit(f"{SEARCH_LIMIT}" if args.limiter else None)
@login_required
def search():
    # Fetch cities for the initial rendering of the form
    cities = cursor_fetch('SELECT DISTINCT city FROM cities')

    # Get user data
    user_id = session['user_id']

    if request.method == 'POST':
        # Get user submitted form data
        house_type = request.form.get('houseType')
        square_meters = json.loads(request.form.get('squareMeters'))
        rental = json.loads(request.form.get('rental'))
        bedrooms = json.loads(request.form.get('bedrooms'))
        bathrooms = json.loads(request.form.get('bathrooms'))
        city = request.form.get('city')
        municipality = request.form.get('municipality')
        region = request.form.get('region')
        tolerance = int(request.form.get('tolerance'))
        exposure = 'public'

        try:
            # Ensure user form input for search submissions is valid
            search_validation(
                exposure,
                house_type,
                square_meters,
                rental,
                bedrooms,
                bathrooms,
                city,
                municipality,
                region
            )

            # Fetch desired destination according to user's submissions
            query = '''
                    SELECT *
                    FROM submissions
                    WHERE user_id = ?;
                    '''
            user_submission = cursor_fetch(
                query,
                user_id
            )

            # Fetch all submissions from database according to search filters
            query = '''
                    SELECT submissions.*,
                        users.email,
                        users.username,
                        regions.postal_code
                    FROM submissions
                    JOIN users ON submissions.user_id = users.id
                    JOIN regions ON submissions.region = regions.region
                    WHERE (submissions.house_type = ? OR ? = '')
                    AND ((submissions.square_meters >= ?
                        AND submissions.square_meters <= ?)
                        OR ? IS NULL OR ? = '')
                    AND ((submissions.rental >= ? 
                        AND submissions.rental <= ?)
                        OR ? IS NULL OR ? = '')
                    AND ((submissions.bedrooms >= ? 
                        AND submissions.bedrooms <= ?)
                        OR ? IS NULL OR ? = '')
                    AND ((submissions.bathrooms >= ?
                        AND submissions.bathrooms <= ?)
                        OR ? IS NULL OR ? = '')
                    AND (submissions.city = ? OR ? = '')
                    AND (submissions.municipality = ? OR ? = '')
                    AND (submissions.region = ? OR ? = '')
                    AND submissions.exposure = ?
                    AND submissions.user_id != ?;
                    '''

            # Execute the query with the provided parameters
            search_results = cursor_fetch(
                query,
                house_type, house_type,
                square_meters['min'], square_meters['max'],
                square_meters['min'], square_meters['max'],
                rental['min'], rental['max'],
                rental['min'], rental['max'],
                bedrooms['min'], bedrooms['max'],
                bedrooms['min'], bedrooms['max'],
                bathrooms['min'], bathrooms['max'],
                bathrooms['min'], bathrooms['max'],
                city, city,
                municipality, municipality,
                region, region,
                exposure,
                user_id)

            # Define function to determine location match strength
            def determine_location_match_strength(result, user_submission):
                location_match_strength = 0

                # Check if desired city destination matches in search results
                if result['city_destination'] == 'any':
                    location_match_strength += 1
                if user_submission[0]['city_destination'] == result['city']:
                    location_match_strength += 2
                if result['city_destination'] == user_submission[0]['city']:
                    location_match_strength += 2


                # Check if desired municipality destination matches in search results
                if (
                    result['municipality_destination'] == 'any'
                ) and (
                    result['city_destination'] == user_submission[0]['city']
                ):
                    location_match_strength += 1
                if user_submission[0]['municipality_destination'] == result['municipality']:
                    location_match_strength += 2
                if result['municipality_destination'] == user_submission[0]['municipality']:
                    location_match_strength += 2

                # Check if desired region destination matches in search results
                if (
                    result['region_destination'] == 'any'
                ) and (
                    result['city_destination'] == user_submission[0]['city']
                ) and (
                    result['municipality_destination'] == user_submission[0]['municipality']
                ):
                    location_match_strength += 1
                if user_submission[0]['region_destination'] == result['region']:
                    location_match_strength += 2
                if result['region_destination'] == user_submission[0]['region']:
                    location_match_strength += 2

                return location_match_strength

            # Function to perform location matching and assign match strength
            def perform_location_matching(user_submission, search_results):
                for result in search_results:
                    location_match_strength = determine_location_match_strength(result, user_submission)
                    result['location_match'] = location_match_strength

            # Call the perform_location_matching function in your route
            perform_location_matching(user_submission, search_results)
            i = 1
            for result in search_results:
                print(i, ": ", result['location_match'])
                i += 1


            TOLERANCE_MULTIPIERS = {
                'square_meters': (tolerance / 100) + 1,
                'rental': (tolerance / 100) + 1,
                'bedrooms': 1 if tolerance < 50 else 2,
                'bathrooms': 1 if tolerance < 70 else 2
            }
            

            # Function to determine match strength based on criteria
            def determine_match_strength(result, user_submission):
                CRITERIA_RANGES = {
                    'square_meters':
                    {
                        'min': result['square_meters'] - ((TOLERANCE_MULTIPIERS['square_meters'] * result['square_meters']) % result['square_meters']),
                        'max': result['square_meters'] * TOLERANCE_MULTIPIERS['square_meters']
                    },
                    'rental':
                    {
                        'min': result['rental'] - ((TOLERANCE_MULTIPIERS['rental'] * result['rental']) % result['rental']),
                        'max': result['rental'] * TOLERANCE_MULTIPIERS['rental']
                    },
                    'bedrooms':
                    {
                        'min': result['bedrooms'] - 1,
                        'max': result['bedrooms'] + 1
                    },
                    'bathrooms':
                    {
                        'min': result['bathrooms'] - 1,
                        'max': result['bathrooms'] + 1
                    }
                }


                house_details_match_strength = 0

                for criteria, ranges in CRITERIA_RANGES.items():
                    print(criteria)
                    print(ranges)
                    if ranges['min'] <= user_submission[0][criteria] <= ranges['max']:
                        house_details_match_strength += 10
                return house_details_match_strength



            # Function to perform matching and assign match strength to each submission
            def perform_house_matching(user_submission, search_results):
                for result in search_results:
                    # print(result['square_meters'])
                    # pp.pprint(user_submission[0]['square_meters'])
                    # # Define matching criteria ranges
                    
                    house_details_match_strength = determine_match_strength(result, user_submission)
                    result['house_details_match'] = house_details_match_strength

            # Call the perform_matching function in your route
            perform_house_matching(user_submission, search_results)
            i = 1
            for result in search_results:
                print(i, ": ", result['house_details_match'])
                i += 1






            return render_template(
                '/search.html',
                cities=cities,
                search=search_results,
                comma=comma,
                whitespace=whitespace
            )
        except ValueError as err:
            # Update log with ERROR msg
            log(
                f'''
                {session['ip']}
                USER[{session['username']}]: FAILED: Search submissions 'aborted': {err}
                ''',
                level='WARNING',
                indent=20
            )

            # Reload search page with default options selected
            return render_template(
                '/search.html',
                cities=cities,
                search_initial_page_load = True,
                search=None,
                error=err,
                whitespace=whitespace
            )
    else:
        # Update log with INFO msg
        log(
            f'''
            {session['ip']}
            USER[{session['username']}]: NAVIGATION: @search.html
            ''',
            indent=24
        )

        return render_template(
            '/search.html',
            cities=cities,
            search_initial_page_load = True,
            search=None,
            whitespace=whitespace
        )


# |----- ACCOUNT HTML ROUTE ----|
@app.route('/account')
@login_required
def account():
    # Update log with INFO msg
    log(
        f'''
        {session['ip']}
        USER[{session['username']}]: NAVIGATION: @account.html
        '''
    )
    return render_template('/account.html')


# |----- PASSWORD RESET POST BUTTON ROUTE ----|
@app.route('/password_reset', methods=['POST'])
@limiter.limit(f"{PASSWORD_RESET_LIMIT}" if args.limiter else None)
@login_required
def password_reset():
    # Get user data
    user_id = session['user_id']

    # Get user submitted form data
    old_password = request.form.get('oldPassword')
    new_password = request.form.get('newPassword')
    confirm_new_password = request.form.get('confirmNewPassword')

    # Fetch user hash
    query = '''
            SELECT hash FROM users
            WHERE id = ?;
            '''
    hash = cursor_fetch(query, user_id)

    try:
        password_reset_validation(
            old_password,
            new_password,
            confirm_new_password,
            hash
        )

        # Hash new password before storing it
        hashed_new_password = generate_password_hash(
            new_password,
            method='scrypt',
            salt_length=16
        )

        # Update new hashed password in the database
        query = '''
                UPDATE users
                SET hash = ?
                WHERE id = ?;
                '''
        cursor_execute(query, hashed_new_password, user_id)

        # Update log with INFO msg
        log(
            f'''
            {session['ip']}
            USER[{session['username']}]: SUCCESS: Password 'changed'
            ''',
            indent=24
        )

    except ValueError as err:
        # Update log with ERROR msg
        log(
            f'''
            {session['ip']}
            USER[{session['username']}]: FAILED: Password 'reset': {err}
            ''',
            level='WARNING',
            indent=24
        )

        return render_template('/account.html', error=err)

    # Inform user for successful password change
    message = {
        'success': 'Password successfully changed!'
    }
    flash(message)
    return render_template('/account.html')


# |----- UPDATE USERNAME POST BUTTON ROUTE ----|
@app.route('/update_username', methods=['POST'])
@limiter.limit(f"{UPDATE_USERNAME_LIMIT}" if args.limiter else None)
@login_required
def update_username():
    # Get user data
    user_id = session['user_id']
    old_username = session['username']

    # Get user submitted form data
    new_username = request.form.get('newUsername').lower()

    try:
        # Ensure user form input for update password is valid
        update_username_validation(
            new_username,
            user_id
        )

        # Update exposure value in the database
        query = '''
                UPDATE users
                SET username = ?
                WHERE id = ?
                '''
        cursor_execute(
            query,
            new_username,
            user_id
        )
        session['username'] = new_username

        # Update log with INFO msg
        log(
            f'''
            {session['ip']}
            USER[{session['username']}]: SUCCESS: Username 'updated': '{old_username}' -> '{new_username}'
            ''',
            indent=24
        )

    except (ValueError, NameError) as err:
        # Update log with ERROR msg
        log(
            f'''
            {session['ip']}
            USER[{session['username']}]: FAILED: Username update 'aborted': {err}
            ''',
            level='WARNING',
            indent=24
        )

        if isinstance(err, ValueError):
            return render_template('/account.html', error=err)
        elif isinstance(err, NameError):
            return render_template('/account.html', warning=err)

    # Inform user for successful username update
    message = {
        'success': 'Username successfully changed!'
    }
    flash(message)
    return render_template('/account.html')


# |----- DELETE ACCOUNT POST BUTTON ROUTE ----|
@app.route('/delete_account', methods=['POST'])
@limiter.limit(f"{DELETE_ACCOUNT_LIMIT}" if args.limiter else None)
@login_required
def delete_account():
    # Get user data
    user_id = session['user_id']

    # Get user submitted form data
    delete_account_confirmation = request.form.get('deleteAccountConfirmation')

    # Fetch user hash
    query = '''
            SELECT email FROM users
            WHERE id = ?;
            '''
    email = cursor_fetch(query, user_id)

    try:
        delete_account_validation(
            delete_account_confirmation,
            email,
        )

        # Delete any user sumbission from database
        query = '''
                DELETE FROM submissions
                WHERE user_id = ?;
                '''
        cursor_execute(query, user_id)

        # Delete any user sumbission from database
        query = '''
                DELETE FROM users
                WHERE id = ?;
                '''
        cursor_execute(query, user_id)

        # Update log with INFO msg
        log(
            f'''
            {session['ip']}
            USER[{session['username']}]: SUCCESS: User account and submissions 'deleted'
            ''',
            indent=24
        )

    except ValueError as err:
        # Update log with ERROR msg
        log(
            f'''
            {DATETIME}:{session['ip']}
            USER[{session['username']}]: FAILED: Account deletion 'aborted': {err}
            ''',
            level='WARNING',
            indent=24
            )
        
        return render_template('/account.html', error=err)

    session.clear()

    # Inform user for successful account deletion
    message = {
        'success': 'Your account and data has been erased. Thanks for using our app!'
    }
    flash(message)
    return render_template('/signup.html')


# |----- ABOUT HTML ROUTE ----|
@app.route('/about')
@login_required
def about():
    return render_template('/about.html')


if __name__ == '__main__':
    app.run(debug=True if args.debug else False)
