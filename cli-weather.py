
from configparser import ConfigParser
from argparse import *


# create function for parsing args passed to CLI
def parse_args():
    argParser = ArgumentParser(description= "Return weather/forecast for the near future (~4 days) for a city.")
    
    argParser.add_argument("City", nargs="+", type=str, help="entered city name must not contain spelling errors")
    argParser.add_argument("-i", "--imperial", action="store_true", help="change display mode to Fahrenheit.")

    return argParser.parse_args()


if __name__ == "__main__":
    parse_args()


