import requests
import os
import time
from datetime import datetime

def get_weather_data(city, api_key):
    # interact with openweather api
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    # make sure temperature is in celsius with metric
    complete_url = f"{base_url}appid={api_key}&q={city}&units=metric"
    response = requests.get(complete_url)
    return response.json()

def display_cursor():
    # display spinning cursor while awaiting new weather info
    while True:
        for cursor in '|/-\\':
            yield cursor

def format_weather_data(weather_data):
    # update weather json data from api
    main_data = weather_data["main"]
    temperature = main_data["temp"]
    pressure = main_data["pressure"]
    humidity = main_data["humidity"]
    weather_description = weather_data["weather"][0]["description"]
    return temperature, pressure, humidity, weather_description

def append_to_file(filename, data):
    with open(filename, "a") as file:
        file.write(data + "\n")

def main():
    # set api key as environment variable !!!!
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        print("Error: No API key found. Set the OPENWEATHER_API_KEY environment variable.")
        return

    # set city name
    city = input("Enter city name: ")
    # set filename using city and datetime for organization
    filename = f"weather_{city}_{datetime.now().strftime('%Y%m%d %H%M%S')}.txt"
    spinner = display_cursor()

    last_weather = None
    while True:
        weather_data = get_weather_data(city, api_key)

        # if invalid, return and error
        if weather_data.get("cod") != 200:
            print(f"Error fetching weather data: {weather_data.get('message', 'Unknown Error')}")
            return

        current_weather = format_weather_data(weather_data)
        if current_weather != last_weather:
            last_weather = current_weather
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # clear spinner
            weather_info = f"[{timestamp}] {city}: {current_weather[0]}°C, {current_weather[1]}hPa, humidity {current_weather[2]}%, {current_weather[3]}"
            print(" " * 10, end='\r')
            print(f'{weather_info}')
            append_to_file(filename, weather_info)
        else:
            print(next(spinner), end='\r')

        # check every 2 seconds for updates
        time.sleep(2)

if __name__ == "__main__":
    main()