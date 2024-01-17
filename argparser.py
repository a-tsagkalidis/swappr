import argparse
parser = argparse.ArgumentParser(description="Swappr: Swap your house and move to your region of favor.")

parser.add_argument('-d', '--debug', action='store_true', help="run Flask in debug mode")
parser.add_argument('-b', '--backup', action='store_true', help="run with Flask Limiter mode")
parser.add_argument('-l', '--limiter', action='store_true', help="run with Flask Limiter mode")

args = parser.parse_args()