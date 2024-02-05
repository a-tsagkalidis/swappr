import re
import string
from fhelpers import email_exists, strong_password, username_exists 

def signup_validation(email, username, password, confirm_password):
    '''
    Checks for valid user input form in signup route.
    '''
    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 20

    # Ensure fields are not blank
    if not email or not username or not password or not confirm_password:
        raise ValueError('Please fill in all the required fields.')
    
    # Ensure email does not contain invalid email characters and has valid structure
    email_regex_stipulations = re.compile(
        r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    if not email_regex_stipulations.match(email):
        raise ValueError('Please enter a valid email address.')

    # Ensure password and confirmation match
    if password != confirm_password:
        raise ValueError('Password and password confirmation do not match.')

    # Ensure new username does not fall short the minimum length
    if len(username) < MIN_USERNAME_LENGTH:
        raise ValueError(
            f'''
            Username must be at least {MIN_USERNAME_LENGTH} characters long.
            '''
        )
    
    # Ensure new username does not exceed the maximum length
    if len(username) > MAX_USERNAME_LENGTH:
        raise ValueError(
            f'''
            Username cannot exceed {MAX_USERNAME_LENGTH} characters.
            '''
        )

    # Ensure username does not contain punctuation characters or whitespaces
    if any(char in string.punctuation or char.isspace() for char in username):
        raise ValueError(
            'Username cannot contain punctuation characters or whitespaces.'
        )

    # # Ensure password is strong
    if not strong_password(password):
        raise ValueError(
            '''
            Password must be at least 8 characters long, including at least 1
            uppercase letter, 1 lowercase letter, a decimal number, and a
            punctuation character.
            '''
        )

    # Ensure email does not exist
    if email_exists(email):
        raise ValueError(
            '''
            The provided email address is already in use. Please choose a 
            different one.
            '''
        )

    # Ensure username does not exist
    if username_exists(username):
        raise ValueError(
            '''
            The chosen username is already in use. Please choose a different
            one.
            '''
        )

    # Validation successfully passed
    return True
