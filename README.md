# cli-weather-app

This is a weather app that can be executed from the command line interface(CLI). Additionally, it may (optionally) fetch the 5-day forecast for the chosen city (in 3-hour periods). The app makes use of various free-to-use REST APIs provided by [OpenWeather](https://openweathermap.org/api). </br></br>
The [Geocoder API](https://openweathermap.org/current#geocoding) helps the user streamline their search by returning a list of all cities with duplicate names. The [Forecast API](https://openweathermap.org/forecast5#multi) uses the latitude and longitude of the selected city to build the endpoint request.</br></br>
The weather output has been styled using python libraries and emojis for increased visual appeal and readability. Furthermore, users can have the app return weather descriptions in their target language. </br>

Please use the following codes corresponding to possible target languages: 


    af - Afrikaans
    al - Albanian
    ar - Arabic
    az - Azerbaijani
    bg - Bulgarian
    ca - Catalan
    cz - Czech
    da - Danish
    de - German
    el - Greek
    en - English
    eu - Basque
    fa - Persian (Farsi)
    fi - Finnish
    fr - French
    gl - Galician
    he - Hebrew
    hi - Hindi
    hr - Croatian
    hu - Hungarian
    id - Indonesian
    it - Italian
    ja - Japanese
    kr - Korean
    la - Latvian
    lt - Lithuanian
    mk - Macedonian
    no - Norwegian
    nl - Dutch
    pl - Polish
    pt - Portuguese
    pt_br - Português Brasil
    ro - Romanian
    ru - Russian
    sv, se - Swedish
    sk - Slovak
    sl - Slovenian
    sp, es - Spanish
    sr - Serbian
    th - Thai
    tr - Turkish
    ua, uk - Ukrainian
    vi - Vietnamese
    zh_cn - Chinese Simplified
    zh_tw - Chinese Traditional
    zu - Zulu

It is important to note that not all cities have different names in different languages, and certain cities do not have weather data available (in which case, the app returns a 404 error).


