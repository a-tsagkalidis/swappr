import argparse
parser = argparse.ArgumentParser(description="Swappr: Swap your house and move to your region of favor.")

parser.add_argument('-d', '--debug', action='store_true', help="run flask in debug mode")
parser.add_argument('-b', '--backup', action='store_true', help="backups database and logs")
parser.add_argument('-l', '--limiter', action='store_true', help="run flask limiter mode")
parser.add_argument('-m', '--mockupsgen', action='store', type=int, nargs=2, help="generates and inserts given number of user and submission mockups in database for testing purposes")
parser.add_argument('-p', '--premademockups', action='store_true', help="inserts a JSON of users and submission in the database that can test all possible matching scores")

argparser = parser.parse_args()
