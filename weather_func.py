import os
import requests
import json
from replit import db
from dotenv import load_dotenv

# function to get weather information.

load_dotenv()
api_key = os.getenv('APIKEY')
base_url = "http://api.openweathermap.org/data/2.5/weather?"
print(api_key)


def get_weather(city, type="$feel"):
    # generating url for given city name.
    complete_url = base_url + "appid=" + api_key + "&q=" + city
    response = requests.get(complete_url)
    data = json.loads(response.text)
    # data = response.json() //// this works too.....

    # if data["cod"] == "404", city not found in API.

    if data["cod"] != "404":
        main = data["main"]
        # weather attributes.
        feel = main["feels_like"]

        temp = main["temp"]
        pres = main["pressure"]
        hum = main["humidity"]
        min_temp = main["temp_min"]
        max_temp = main["temp_max"]
        # for descriptons like cloudy sky, clear sky etc.
        weather = data["weather"]
        weather_des = weather[0]["description"]
        if type == "$table":
            if db["units"] == "CA":
                toShow = f'''
                    {city:-^40}\nTemperature varies from {(float(min_temp) - 273.16):.2f} to {(float(max_temp) - 273.16):.2f} degrees celsius,\nPressure is {(pres/1013.25):.2f} atm,\nHumidity is {hum}%,\nDescription --> {weather_des}.
            '''
            elif db["units"] == "KH":
                toShow = f'''
                    {city:-^40}\nTemperature varies from {(float(min_temp)):.2f} to {(float(max_temp)):.2f} kelvin,\nPressure is {pres} hPa,\nHumidity is {hum}%,\nDescription --> {weather_des}.
            '''
        elif type == "$describe":
            if db["units"] == "CA":
                toShow = f'''
                    The weather for {city} shows a temperature of {(float(temp) - 273.16):.2f} degrees celsius,\nwith the pressure being {(pres/1013.25):.2f} atm,\nHumidity is {hum}%,\nand it is {weather_des}.
            '''
            elif db["units"] == "KH":
                toShow = f'''
                    The weather for {city} shows a temperature of {(float(temp)):.2f} kelvin,\nwith the pressure being {(pres):.2f} hPa,\nHumidity is {hum}%,\nand it is {weather_des}.
            '''
        elif type == "$feel":
            if db["units"] == "CA":
                toShow = f'''
                    Feels like {(float(feel) - 273.16):.2f} degrees celsius in {city}.
            '''
            elif db["units"] == "KH":
                toShow = f'''
                    Feels like {float(feel):.2f} kelvin in {city}. 
            '''

        return(toShow)
    else:
        return("City Not Found.")
