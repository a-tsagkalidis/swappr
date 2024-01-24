import argparse
parser = argparse.ArgumentParser(description="Swappr: Swap your house and move to your region of favor.")

parser.add_argument('-d', '--debug', action='store_true', help="run flask in debug mode")
parser.add_argument('-b', '--backup', action='store_true', help="backups database and logs")
parser.add_argument('-l', '--limiter', action='store_true', help="run flask limiter mode")
parser.add_argument('-o', '--obfuscate', action='store_true', help="obfuscates javascript file")

args = parser.parse_args()
