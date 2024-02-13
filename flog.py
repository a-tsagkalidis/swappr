import json
from loguru import logger


def log(message, level='INFO', indent=28):
    '''
    Dynamically handles log indentations and message level.
    '''
    message = '\n'.join([' ' * indent + line for line in message.splitlines()])
    logger.log(
        level,
        message,
    )


def initialize_logger():
    '''
    Initializes loguru history logger.
    '''
    logger.add(
        'app.log',
        format="{level}:swappr:[{time:DD/MMM/YYYY HH:mm:ss}]: {message}",
        colorize=True,
        backtrace=True,
        diagnose=True
    )


def log_new_locations(locations_update, new_locations_flag):
    '''
    Add brief log info about newly inserted location entries in the database.
    '''
    if new_locations_flag:
        # Updage log with WARNING msg
        log(
            f'''
            App initialized successfully. Database tables where created
            in case they weren't exist. JSON file with locations has been
            imported to the database - NEWLY IMPORTED LOCATIONS: 
            {json.dumps(locations_update, indent=8)}
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
        