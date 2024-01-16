from flask import Flask, render_template, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from flask_limiter.util import get_remote_address
from flask_limiter import Limiter
from supportive_functions import *
from datetime import datetime
from argparser import args
import logging
import secrets
import json
import sys
import os

# Flask instance to initialize the web application.
app = Flask(__name__)

# Flask limiter instance for spam request protection
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

os.system('bash log.sh')

# Configure logging
logging.basicConfig(filename='app.log', level=logging.ERROR)

# Declare a secret key for Flask application - it is needed for flash function
app.secret_key = secrets.token_hex(32)

# Initialize the database and tables
create_database_tables()

# Import location data from locations.json file into proper database tables
location_update, flag = import_locations()

# In case of newly imported locations in the database inform properly the log
if flag:
    # Updage log with WARNING msg
    app.logger.setLevel(logging.WARNING)
    app.logger.warning(
        f'''
        App initialized successfully. Database tables where created
        in case they weren't exist. JSON file with locations has been
        imported to the database - NEWLY IMPORTED LOCATIONS: {
            json.dumps(location_update, indent=2)
            }
        '''
    )
else:
    # Updage log with INFO msg
    app.logger.setLevel(logging.INFO)
    app.logger.info(
        '''
        App initialized successfully. Database tables where created
        in case they weren't exist. JSON file with locations has been
        imported to the database - NO NEWLY IMPORTED LOCATIONS FOUND.
        '''
    )


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
    app.logger.info(
        f'''
        User with username `{session['username']}` and user_id 
        {session['user_id']} navigation @index.html
        '''
    )
    return render_template(
        'index.html',
        submissions=submissions_data,
        comma=comma,
        whitespace=whitespace
    )


@app.route('/signup', methods=['GET', 'POST'])
@limiter.limit("50/minute")
def signup():
    if request.method == 'POST':
        # Get user submitted form data
        email = request.form.get('email').lower()
        username = request.form.get('username').lower()
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')

        # Check if all form fields are filled and valid, else flash error and reload the route
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

            # Sign up new user and then sign in
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
            signin()

            # Update log with INFO msg
            app.logger.info('New user successfuly registered in database')

            # Inform the user for successful register
            flash('Successfully registered!')
            return redirect(url_for('delayed_redirect'))

        except ValueError as err:
            # Update log with ERROR msg
            app.logger.error(f'Signup failed: {err}')
            return render_template('/signup.html', error=err)

    # Update log with INFO msg
    app.logger.info('User navigation @signup.html')
    return render_template('/signup.html')


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
    app.logger.info('New user redirected @index.html')

    # Render the delayed redirect template with a JavaScript redirect
    return render_template('delayed_redirect.html')


@app.route("/signin", methods=['GET', 'POST'])
@limiter.limit("50/minute")
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

        # Check if all form fields are filled and valid, else flash error and reload the route
        try:
            # Ensure user form input for signin is valid
            signin_validation(
                username,
                password,
                user_data
            )

            # Remember user_id and username of the user who has logged in
            session['user_id'] = user_data[0]['id']
            session['username'] = user_data[0]['username']
            session['email'] = user_data[0]['email']

            # Update log with INFO msg
            app.logger.info(
                f'''
                User with username `{session['username']}` and user_id 
                {session['user_id']} just signed in.
                '''
            )

            # Redirect user to home page
            return redirect('/')

        except ValueError as err:
            # Update log with ERROR msg
            app.logger.error(f'Signin failed: {err}')
            return render_template('/signin.html', error=err)


    # Update log with INFO msg
    app.logger.info('Visitor navidation @signin.html')
    return render_template('/signin.html')


@app.route('/signout')
@login_required
def signout():
    # Update log with INFO msg
    app.logger.info(
        f'''
        User with username `{session['username']}` and user_id 
        {session['user_id']} just signed out.
        '''
    )

    # Forget any user_id
    session.clear()
    return redirect('/')


@app.route('/submit', methods=['GET', 'POST'])
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
        all_field_values = list(request.form.values())

        # Check if all form fields are filled and valid, else flash error and reload the route
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
            )
            # Update log with WARNING msg
            app.logger.warning('Submission validated successfully.')

            # Save submission into user database
            query = '''
                    INSERT INTO submissions (
                        user_id,
                        house_type,
                        square_meters,
                        rental,
                        bedrooms,
                        bathrooms,
                        exposure,
                        city,
                        municipality,
                        region
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    '''
            cursor_execute(
                query,
                user_id,
                house_type,
                square_meters,
                rental,
                bedrooms,
                bathrooms,
                exposure,
                city,
                municipality,
                region
            )

            # Update log with INFO msg
            app.logger.info(
                f'''
                User with username `{session['username']}` and user_id 
                {user_id} successfully saved a new sumbission
                '''
            )

            # Inform user for successful submission
            flash('Submission saved successfully!')
            return redirect('/')

        except ValueError as err:
            # Update log with ERROR msg
            app.logger.error(
                f'''
                User with username `{session['username']}` and user_id 
                {user_id} ERROR: Submission failed: {err}
                '''
            )
            return render_template(
                '/submit.html',
                submission=None,
                error=err
            )

    else:
        # Update log with INFO msg
        app.logger.info(
            f'''
            User with username `{session['username']}` and user_id 
            {user_id} navigation @submit.html
            '''
        )

        return render_template(
            '/submit.html',
            cities=cities,
            submission=None,
            whitespace=whitespace
        )


@app.route('/update_exposure', methods=['POST'])
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
    app.logger.info(
        f'''
        User with username `{session['username']}` and user_id 
        {user_id} changed exposure to `{new_exposure}` status for 
        submission with submission_id {submission_id}
        '''
    )

    flash('Exposure updated successfully!')
    return redirect(url_for('index'))


@app.route('/edit_submission', methods=['POST'])
@login_required
def edit_submission():
    # Fetch cities for the initial rendering of the form
    cities = cursor_fetch('SELECT DISTINCT city FROM cities')

    # Get user data
    user_id = session['user_id']

    # Retrieve data from the form
    submission_id = request.form.get('submission_id')

    # Check if the submission exists by fetchin it
    query = '''
            SELECT * FROM submissions
            WHERE id = ?
            AND user_id = ?;
            '''
    submission_data = cursor_fetch(query, submission_id, user_id)

    # If submission exists pass its data to the edit page, else reload index route
    if submission_data:
        # Update log with INFO msg
        app.logger.info(
            f'''
            User with username `{session['username']}` and user_id {user_id} 
            navigation @edit_submission.html and editing submission with 
            submission_id {submission_id}
            '''
        )

        return render_template(
            '/edit_submission.html',
            cities=cities,
            submission=submission_data[0],
            whitespace=whitespace,
        )
    else:
        # Update log with ERROR msg
        app.logger.error(
            f'''
            User with username `{session['username']}` and user_id {user_id} 
            ERROR: Submission with submission_id {submission_id} not found
            '''
        )

        flash('Submission not found.')
        return redirect(url_for('index'))


@app.route('/edited_submission', methods=['POST'])
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
    all_field_values = list(request.form.values())

    # Save edited house or delete it
    if 'save' in request.form:
        # Check if all form fields are filled and valid, else flash error and reload the route
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
            )
            # Update log with WARNING msg
            app.logger.warning(
                f'''
                User with username `{session['username']}` and user_id {user_id} 
                successfully VALIDATED input for editing submission_id {submission_id}
                '''
            )

            # Update edited submission into user database
            query = '''
                    UPDATE submissions SET
                        house_type = ?,
                        square_meters = ?,
                        rental = ?,
                        bedrooms = ?,
                        bathrooms = ?,
                        exposure = ?,
                        city = ?,
                        municipality = ?,
                        region = ?
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
                exposure,
                city,
                municipality,
                region,
                submission_id,
                user_id
            )

            # Update log with INFO msg
            app.logger.info(
                f'''
                User with username `{session['username']}` and user_id {user_id} 
                successfully UPDATED submission with submission_id {submission_id}
                '''
            )

            # Inform user for successful submission update
            flash('Submission updated successfully!')
            return redirect(url_for('index'))

        except ValueError as err:
            # Update log with ERROR msg
            app.logger.error(
                f'''
                User with username `{session['username']}` and user_id {user_id} 
                ERROR: Submission UPDATE failed: {err}
                '''
            )

            # Fetch edited submission data to reload route with correct field valuess
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
        app.logger.info(
            f'''
            Submission with submission_id {submission_id} that
            belonged to user with username `{session['username']} and
            user_id {user_id} has been successfully deleted.
            '''
        )

        # Inform user for successful submission deletion
        flash('Submission deleted successfully!')
        return redirect(url_for('index'))


@app.route('/get_municipalities', methods=['GET'])
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


@app.route('/get_regions', methods=['GET'])
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


@app.route('/search', methods=['GET', 'POST'])
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
        exposure = 'public'
        # TODO: Will be used for validation
        all_field_values = list(request.form.values())

        query = '''
                SELECT submissions.*, users.email, users.username, regions.postal_code FROM submissions
                JOIN users ON submissions.user_id = users.id
                JOIN regions ON submissions.region = regions.region
                WHERE (submissions.house_type = ? OR ? = '')
                AND ((submissions.square_meters >= ? AND submissions.square_meters <= ?) OR ? IS NULL OR ? = '')
                AND ((submissions.rental >= ? AND submissions.rental <= ?) OR ? IS NULL OR ? = '')
                AND ((submissions.bedrooms >= ? AND submissions.bedrooms <= ?) OR ? IS NULL OR ? = '')
                AND ((submissions.bathrooms >= ? AND submissions.bathrooms <= ?) OR ? IS NULL OR ? = '')
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

        return render_template(
            '/search.html',
            cities=cities,
            search=search_results,
            comma=comma,
            whitespace=whitespace
        )
    else:
        # Update log with INFO msg
        app.logger.info(
            f'''
            User with username `{session['username']}` and user_id
            {user_id} navigation @search.html
            '''
        )

        return render_template(
            '/search.html',
            cities=cities,
            search_initial_page_load = True,
            search=None,
            whitespace=whitespace
        )


@app.route('/account', methods = ['GET'])
@login_required
def account():
    # Update log with INFO msg
    app.logger.info(
        f'''
        User with username `{session['username']}` and user_id 
        {session['user_id']} navigation @account.html
        '''
    )
    return render_template('/account.html')


@app.route('/password_reset', methods=['POST'])
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
        app.logger.info(
            f'''
            User with username `{session['username']}` and user_id
            {user_id} changed password.
            '''
        )

    except ValueError as err:
        # Update log with ERROR msg
        app.logger.error(f'Password reset failed: {err}')
        return render_template('/account.html', error=err)

    flash('Password successfully changed!')
    return render_template('/account.html')


@app.route('/update_username', methods=['POST'])
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
        app.logger.info(
            f'''
            User with username `{old_username}` and user_id {user_id}
            updated username to `{new_username}`.
            '''
        )

    except (ValueError, NameError) as err:
        # Update log with ERROR msg
        app.logger.error(f'Update username failed: {err}')
        if isinstance(err, ValueError):
            return render_template('/account.html', error=err)
        elif isinstance(err, NameError):
            return render_template('/account.html', warning=err)

    flash('Username successfully changed!')
    return render_template('/account.html')


@app.route('/delete_account', methods=['POST'])
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
        app.logger.info(
            f'''
            User with username `{session['username']}` and user_id
            {user_id} has been deleted from database. All user's sumbissions
            has been deleted.
            '''
        )

    except ValueError as err:
        # Update log with ERROR msg
        app.logger.error(f'Account deletion failed: {err}')
        return render_template('/account.html', error=err)

    session.clear()
    flash('Your account and data has been erased. Thanks for using our app!')
    return render_template('/signup.html')


if __name__ == '__main__':
    app.run(debug=True if args.debug else False)
