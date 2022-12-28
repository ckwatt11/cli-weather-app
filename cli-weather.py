import json
import pprint
import sys
from style import *
from configparser import ConfigParser
from urllib import error, request, parse
from argparse import *

OUTPUT_PADDING = 20

API_ACCESS_LINK = "http://api.openweathermap.org/data/2.5/weather" # content appended to link will be user input that will build the endpoint query. 

GEOCODING_API_LINK = "http://api.openweathermap.org/geo/1.0/direct" # helps return a list of all cities with the same name.

API_FORECAST_ACCESS_LINK = "http://api.openweathermap.org/data/2.5/forecast" # link for fetching forecast (if requested) of selected city.

# Weather Condition Codes
# https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2

THUNDERSTORM = range(200, 300)
DRIZZLE = range(300, 400)
RAIN = range(500, 600)
SNOW = range(600, 700)
ATMOSPHERE = range(700, 800)
CLEAR = range(800, 801)
CLOUDY = range(801, 900)


# create getter for personal API key.

def getApiKey():

    config = ConfigParser()
    config.read("secrets.ini")
    return config["open-weather"]["api_key"]


appId = getApiKey() 


# create function for parsing args passed to CLI
def parse_args():

    argParser = ArgumentParser(description= "Return weather (and optionally the forecast for the near future (~5 days)) for a city.")
    argParser.add_argument("city", nargs="+", type=str, help="entered city name must not contain spelling errors") # allows user to pass multiple whitespace-separated words as city names
    argParser.add_argument("-i", "--imperial", action="store_true", help="change display mode to Fahrenheit.")
    
    return argParser.parse_args()


def constructRequest(city_name, country_code="", isImperial=False):
     
    """ 
    Combine the components back into a URL API request string, and to convert a “relative URL” to an absolute URL given a “base URL.”

    """

    cityNameUrl = parse.quote_plus(city_name) # how city names (should) appear in the URL : 'Sao Paulo' -> 'Sao+Paulo' 
    
    # forecast = 
    units = "imperial" if isImperial else "metric"
    
    apiRequest = API_ACCESS_LINK + "?q={}".format(cityNameUrl) + ",{}".format(country_code) + "&units={}".format(units) + "&appid={}".format(appId)
    return apiRequest

    

def fetchWeather(req):  # return weather data based on the constructed API request URL

    '''
    req -> constructed API request
    '''

    # add error/exception handling for conciseness and readability
    try:
        result = request.urlopen(req) # create GET request
    except error.HTTPError as http_err:
        match http_err:
            case '401':
                sys.exit("Access not authorized. Please check your API key.")
            case '404': 
                sys.exit("No weather information available for this city. Please double-check the name you entered.")
            case default:
                sys.exit("The app encountered an error: {}".format(http_err))    

    weatherInfo = result.read()
    
    try:
        return json.loads(weatherInfo)
    except json.JSONDecodeError:
        sys.exit("Couldn't read server response.\n")



def displayWeather(weather_output_dict, isImperial=False):

    city_name = weather_output_dict['name']
    city_temp = weather_output_dict['main']['temp']
    weather_description = weather_output_dict['weather'][0]['description']
    weather_id = weather_output_dict['weather'][0]['id']
    temp_units = "°F" if isImperial else "°C"
    change_color(REVERSE)
    print(f"\nPlace: {city_name.capitalize():^{OUTPUT_PADDING}}\n")
    print(f"Temperature: {city_temp} {temp_units}\n")
    print(
    f"Weather Description: \t{weather_description.capitalize():^{OUTPUT_PADDING}}\n",
    end=" ",
    )
    change_color(RESET)


def _set_disp_params(wthr_id): # not a public function

    if wthr_id in THUNDERSTORM:
        color = RED

    elif wthr_id in DRIZZLE:
        color = CYAN

    elif wthr_id in RAIN:
        color = BLUE

    elif wthr_id in SNOW:
        color = WHITE

    elif wthr_id in ATMOSPHERE:
        color = BLUE

    elif wthr_id in CLEAR:
        color = YELLOW

    elif wthr_id in CLOUDY:
        color = WHITE
        
    else: 
        color = RESET

    return color;     

def formatCityName(full_city_name, cty):
    string_size = len(cty)
    start_idx = full_city_name.find(cty)
    return full_city_name[start_idx:start_idx + string_size]


if __name__ == "__main__":

    args_passed = parse_args()
    suggestions = GEOCODING_API_LINK + "?q={}".format(args_passed.city[0]) + "&limit=10" + "&appid={}".format(appId)
    geocode_city_options = request.urlopen(suggestions)
    possibilities = geocode_city_options.read()
    possible_cities = json.loads(possibilities)
    
    for i in range(len(possible_cities)):
        print(f"{i} :\t{possible_cities[i]['name']}, {possible_cities[i]['country']}")
    

    
    choice = int(input("Please be more specific (choose a number to validate intended city) : \n").strip())
    chosen_city = possible_cities[choice]['name']
    final_choice = formatCityName(chosen_city, args_passed.city[0])
    country = possible_cities[choice]['country']
    print("You chose: {}, {}".format(chosen_city, possible_cities[choice]['country']))    
    cityWeather = fetchWeather(constructRequest(final_choice, country, args_passed.imperial))


    displayWeather(cityWeather, args_passed.imperial)

    want_forecast = input("\n Would you like to see the 5-day forecast (in 3-hour periods ) for the city? (y/n) \n")
    if (want_forecast == "y" or want_forecast == "Y"):
        f_units = "imperial" if args_passed.imperial else "metric"
        city_forecast_request = API_FORECAST_ACCESS_LINK + "?lat={}".format(cityWeather['coord']['lat']) + "&lon={}".format(cityWeather['coord']['lon']) + "&appid={}".format(appId) + "&units={}".format(f_units)
        city_forecast = request.urlopen(city_forecast_request)
        forecast_info = city_forecast.read()
        fcast_data = json.loads(forecast_info)
        for i in range(40):
            print(f"Period {i + 1} : {fcast_data['list'][i]['main']}\n")
