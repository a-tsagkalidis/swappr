from werkzeug.security import check_password_hash


def signin_validation(username, password, user_data):
    '''
    Checks for valid user input form in signin route.
    '''     
    # Ensure username was submitted
    if not username:
        raise ValueError('Username not entered')

    # Ensure password was submitted
    if not password:
        raise ValueError('Password not entered')
    
    # Ensure username exists and password is correct
    if (
        not user_data
    ) or not (
        check_password_hash(user_data[0]['hash'], password)
    ):
        raise ValueError('Wrong username or password')
    