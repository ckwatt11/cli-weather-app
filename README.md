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


***Help page for the app:***

![helpfile](https://user-images.githubusercontent.com/29700463/210189454-8edef1a8-466b-45ef-8b6f-d0d401d464ec.PNG)


***Sample output in metric units:*** 

![basicmetric](https://user-images.githubusercontent.com/29700463/210189478-b42e8c5b-6711-45f2-80a2-b10df1097215.PNG)


***Sample output in Imperial units:***

![basicimperial](https://user-images.githubusercontent.com/29700463/210189502-f808fd87-98fd-4761-8a65-f0572849572a.PNG)


***Sample output in Ukrainian:***

![ukrainianoutput](https://user-images.githubusercontent.com/29700463/210189521-dcccabf9-0d86-4429-b544-3e3f19ba8ba6.PNG)


***Sample forecast output:***

![forecastimp](https://user-images.githubusercontent.com/29700463/210189657-58d96567-1c35-4b01-828c-cbca5bf2d1e5.PNG)

