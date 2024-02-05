import argparse
parser = argparse.ArgumentParser(description="Swappr: Swap your house and move to your region of favor.")

parser.add_argument('-d', '--debug', action='store_true', help="run flask in debug mode")
parser.add_argument('-b', '--backup', action='store_true', help="backups database and logs")
parser.add_argument('-l', '--limiter', action='store_true', help="run flask limiter mode")
parser.add_argument('-m', '--mockup', action='store', type=int, nargs=2, help="creates and inserts given number of user and submission mockups in database for testing purposes")

args = parser.parse_args()
