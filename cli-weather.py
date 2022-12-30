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
    argParser.add_argument("-l", "--language", nargs=1, type=str, default="en", help="view requested data in specified target language")
    return argParser.parse_args()


def constructRequest(city_name, country_code="", lang="en", isImperial=False):
     
    """ 
    Combine the components back into a URL API request string, and to convert a “relative URL” to an absolute URL given a “base URL.”

    """
    
    cityNameUrl = parse.quote_plus(str(city_name)) # how city names (should) appear in the URL : 'Sao Paulo' -> 'Sao+Paulo' 
    
    # forecast = 
    units = "imperial" if isImperial else "metric"
    
    apiRequest = API_ACCESS_LINK + "?q={}".format(cityNameUrl) + ",{}".format(country_code) + "&units={}".format(units) + "&appid={}".format(appId) + "&lang={}".format(lang)
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
    
    weather_icon, clr = _set_disp_params(weather_id)
    change_color(clr)
    print(
    f"Weather Description: \t{weather_description.capitalize():^{OUTPUT_PADDING}}",
    end=" ",
    )
    print(f" {weather_icon}", end="")
    change_color(RESET)
   


def _set_disp_params(wthr_id): # not a public function

    if wthr_id in THUNDERSTORM:

        display_params = ("💥", RED)

    elif wthr_id in DRIZZLE:

        display_params = ("💧", CYAN)

    elif wthr_id in RAIN:

        display_params = ("💦", BLUE)

    elif wthr_id in SNOW:

        display_params = ("⛄️", WHITE)

    elif wthr_id in ATMOSPHERE:

        display_params = ("🌀", BLUE)

    elif wthr_id in CLEAR:

        display_params = ("🔆", YELLOW)

    elif wthr_id in CLOUDY:

        display_params = ("💨", WHITE)

    else:  # In case the API adds new weather codes

        display_params = ("🌈", RESET)

    return display_params
    

def formatCityName(full_city_name, cty): 
    """
    Formats official city titles into valid search query names. Eg. "Town of Dresden, US (does not return expected output) -> Dresden, US (does)
    """
    string_size = len(cty)
    start_idx = full_city_name.find(cty)
    print(full_city_name[start_idx:start_idx + string_size])


if __name__ == "__main__":

    args_passed = parse_args()
    entered_city_name = args_passed.city
    suggestions = GEOCODING_API_LINK + "?q={}".format(parse.quote_plus(" ".join(args_passed.city))) + "&limit=10" + "&appid={}".format(appId) + "&lang={}".format(args_passed.language[0])
    geocode_city_options = request.urlopen(suggestions)
    possibilities = geocode_city_options.read()
    possible_cities = json.loads(possibilities)
    chosen_lang = args_passed.language[0]
    
    for i in range(len(possible_cities)):
        print(f"{i} :\t{possible_cities[i]['name']}, {possible_cities[i]['country']}")
    

    
    choice = int(input("Please be more specific (choose a number to validate intended city) : \n"))
    chosen_city = possible_cities[choice]['name']
    
    
    try:
        other_name = possible_cities[choice]['local_names'][chosen_lang]
    except KeyError:
        print("This language does not have a (known) unique name for this city; switching to English name. \n")
        other_name = entered_city_name[0] if (len(entered_city_name) == 1) else " ".join(entered_city_name)
    
    country = possible_cities[choice]['country']
    
    print("You chose: {}, {}".format(other_name, possible_cities[choice]['country']))    
    cityWeather = fetchWeather(constructRequest(other_name, country, chosen_lang, args_passed.imperial))
    
    displayWeather(cityWeather, args_passed.imperial)

    want_forecast = input("\n Would you like to see the 5-day forecast (in 3-hour periods ) for the city? (y/n) \n")
    if (want_forecast == "y" or want_forecast == "Y"):
        f_units = "imperial" if args_passed.imperial else "metric"
        city_forecast_request = API_FORECAST_ACCESS_LINK + "?lat={}".format(cityWeather['coord']['lat']) + "&lon={}".format(cityWeather['coord']['lon']) + "&appid={}".format(appId) + "&units={}".format(f_units)
        city_forecast = request.urlopen(city_forecast_request)
        forecast_info = city_forecast.read()
        fcast_data = json.loads(forecast_info)
        for i in range(40):
            print(f"Period {i + 1} : \n temp: {fcast_data['list'][i]['main']['temp']} \n Feels like: {fcast_data['list'][i]['main']['feels_like']} \n Min: {fcast_data['list'][i]['main']['temp_min']} \n Max: {fcast_data['list'][i]['main']['temp_max']} \n Pressure: {fcast_data['list'][i]['main']['pressure']} \n Sea Level: {fcast_data['list'][i]['main']['sea_level']} \n Ground Level: {fcast_data['list'][i]['main']['grnd_level']} \n Humidity: {fcast_data['list'][i]['main']['humidity']} \n")
            
           
