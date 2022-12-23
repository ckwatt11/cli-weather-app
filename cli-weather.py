import json
from configparser import ConfigParser
from urllib import request, parse
from argparse import *

API_ACCESS_LINK = "http://api.openweathermap.org/data/2.5/weather" # appended content to link will be user input that will build the endpoint query. 

#  API_FORECAST_ACCESS_LINK = "https://pro.openweathermap.org/data/2.5/forecast/hourly?{}{}&appid={API key}".format("lat={}&".format(), "lon={}&".format())


# create getter for personal API key.

def getApiKey():

    config = ConfigParser()
    config.read("secrets.ini")
    return config["open-weather"]["api_key"]



# create function for parsing args passed to CLI
def parse_args():

    argParser = ArgumentParser(description= "Return weather/forecast for the near future (~4 days) for a city.")
    argParser.add_argument("city", nargs="+", type=str, help="entered city name must not contain spelling errors") # allows user to pass multiple whitespace-separated words as city names
    argParser.add_argument("-i", "--imperial", action="store_true", help="change display mode to Fahrenheit.")
    return argParser.parse_args()


def constructRequest(city_name, isImperial=False, forecast=False):
     
    """ 
    Combine the components back into a URL string, and to convert a “relative URL” to an absolute URL given a “base URL.”

    """
    appId = getApiKey()
    city = " ".join(city_name)
    cityNameUrl = parse.quote_plus(city) # how city names (should) appear in the URL : 'Sao Paulo' -> 'Sao+Paulo' 
    units = "imperial" if isImperial else "metric"
    apiRequest = API_ACCESS_LINK + "?q={}".format(cityNameUrl) + "&units={}".format(units) + "&appid={}".format(appId)

    return apiRequest
    

       



if __name__ == "__main__":

    args_passed = parse_args()
    print(args_passed.city, args_passed.imperial)
    print(constructRequest(args_passed.city))
    
    



