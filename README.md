# cli-weather-app

This is a weather app that can be executed from the command line interface(CLI). Additionally, it may (optionally) fetch the 5-day forecast for the chosen city (in 3-hour periods). The app makes use of various free-to-use REST APIs provided by [OpenWeather](https://openweathermap.org/api). 
The [Geocoding API](https://openweathermap.org/current#geocoding) helps the user streamline their search by returning a list of all cities with duplicate names. The forecast API uses the latitude and longitude of the selected city to build the endpoint request.
The weather output has been styled using python libraries and emojis for increased visual appeal and readability. 