import string
from flask import session
from werkzeug.security import check_password_hash
from fhelpers import strong_password, username_exists


def password_reset_validation(
        old_password,
        new_password,
        confirm_new_password,
        hash
    ):
    '''
    Checks password reset input validity in account route.
    '''
    # Ensure fields are not blank
    if not old_password or not new_password or not confirm_new_password:
        raise ValueError(
            'Please fill in all the required fields.'
        )
    
    # Ensure old password is correct
    if not check_password_hash(hash[0]['hash'], old_password):
        raise ValueError(
            'Wrong old password'
        )

    # Ensure new password and its confirmation match
    if new_password != confirm_new_password:
        raise ValueError(
            'New password and new password confirmation do not match.'
        )

    # Ensure new password is strong
    if not strong_password(new_password):
        raise ValueError(
            '''
            Password must be at least 8 characters long, including at least 1
            uppercase letter, 1 lowercase letter, a decimal number, and a
            punctuation character.
            '''
        )

    # Validation successfully passed
    return True


def update_username_validation(new_username, user_id):
    '''
    Checks password reset input validity in account route.
    '''
    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 20

    # Ensure field is not blank
    if not new_username:
        raise ValueError(
            'Please fill in all the required field.'
        )

    # Ensure new username does not exist
    if username_exists(new_username, user_id):
        raise ValueError(
            '''
            The chosen username is already in use. Please choose a different
            one.
            '''
        )
    
    # Ensure new username does not fall short the minimum length
    if len(new_username) < MIN_USERNAME_LENGTH:
        raise ValueError(
            f'''
            Username must be at least {MIN_USERNAME_LENGTH} characters
            long.
            '''
        )
    
    # Ensure new username does not exceed the maximum length
    if len(new_username) > MAX_USERNAME_LENGTH:
        raise ValueError(
            f'Username cannot exceed {MAX_USERNAME_LENGTH} characters.'
        )

    # Ensure new username does not contain punctuation chars or whitespaces
    if any(
        char in string.punctuation or
        char.isspace() for char in new_username
    ):
        raise ValueError(
            '''
            Username cannot contain punctuation characters or
            whitespaces.
            '''
        )
    
    # Ensure new username is not the same as the previous one
    if session['username'] == new_username:
        raise NameError(
            'Current username entered. Changes were not saved.'
        )
    

def delete_account_validation(delete_account_confirmation, email):
    '''
    Checks email input validity for account deletion.
    '''
    # Ensure email is valid for username and submissions deletion
    if delete_account_confirmation != email[0]['email']:
        raise ValueError(
            'Wrong email. Account deletion aborted.'
        )
