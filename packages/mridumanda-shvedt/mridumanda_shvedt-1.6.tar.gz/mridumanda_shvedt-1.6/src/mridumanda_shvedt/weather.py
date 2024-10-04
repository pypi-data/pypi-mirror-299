import os
import requests
from datetime import datetime
from rich import print as r_print
from rich.panel import Panel
from rich.columns import Columns
from mridumanda_shvedt.weather_ascii import ascii_arts


def get_city_from_ip():
    try:
        ip_info_response = requests.get("https://ipinfo.io/json")
        
        if ip_info_response.status_code != 200:
            raise Exception("Failed to get location from IP info \nEnter city name manually after the -c flag")
        
        return ip_info_response.json().get('city')
    
    except requests.exceptions.RequestException as e:
        print("Failed to get location from IP info \nEnter city name manually after the -c flag")
        return None


def get_weather(city):
    if city is None:
        city = get_city_from_ip()
    
    API_KEY = get_api_key()
    API_URL = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + API_KEY
    
    try:
        weather_map_response = requests.get(API_URL)
        
        if weather_map_response.status_code is not 200:
            print("Unable to fetch weather data")
            return None
    except requests.exceptions.RequestException as e:
        print("Failed to fetch weather data")
        return None

    weather_data = weather_map_response.json()

    temp = f"{weather_data['main'].get('temp') - 273.15:.2f} °C"
    feels_like = f"{weather_data['main'].get('feels_like') - 273.15:.2f} °C feels like"
    temp_min = f"{weather_data['main'].get('temp_min') - 273.15:.2f} °C"
    temp_max = f"{weather_data['main'].get('temp_max') - 273.15:.2f} °C"
    hum = f"{weather_data['main'].get('humidity')}%"
    pressure = f"{weather_data['main'].get('pressure')} hPa"
    wind_speed = f"{weather_data['wind'].get('speed')} meters per second"
    desc = weather_data['weather'][0].get('description').title()
    visibility = f"{weather_data.get('visibility') / 1000} km"
    id = weather_data['weather'][0].get('id')
    city_name = weather_data['name']
    sunrise, sunset = get_sun_times(weather_data['sys'].get('sunrise'), weather_data['sys'].get('sunset'))
    country = weather_data['sys'].get('country')
    location = f"{city_name}, {country}"

    return [
        [ " ", location, temp, " ", temp_min, temp_max, hum, " ", desc, pressure, " ", id],
        [ " ", location, temp, feels_like, " ", desc, hum, wind_speed, " ", pressure, visibility, f"{sunrise} / {sunset}" ]
    ]


def get_api_key():
    home_dir = os.path.expanduser('~')
    
    if os.name == 'NT':
        api_key_file = os.path.join(home_dir, 'AppData', 'Local', 'mridumanda', 'api_key.txt')
    else:
        api_key_file = os.path.join(home_dir, '.config','mridumanda', 'api_key.txt')
    
    with open(api_key_file, 'r') as f:
        api_key = f.read().split('=')[1].strip()

    return api_key


def get_sun_times(sunrise_timestamp, sunset_timestamp):
    sunrise = datetime.fromtimestamp(sunrise_timestamp)
    sunset = datetime.fromtimestamp(sunset_timestamp)
    
    return sunrise.strftime("%H:%M"), sunset.strftime("%H:%M")


def display_weather_data_ascii(weather_data):
    os.system('clear')
    
    ascii_mapping = {
        range(200, 232): ascii_arts.thunder,
        range(300, 321): ascii_arts.dust,
        range(500, 531): ascii_arts.rain,
        range(600, 622): ascii_arts.snow,
        701: ascii_arts.dust,
        711: ascii_arts.smoke,
        721: ascii_arts.dust,
        731: ascii_arts.dust,
        741: ascii_arts.fog,
        751: ascii_arts.dust,
        761: ascii_arts.dust,
        762: ascii_arts.ash,
        771: ascii_arts.squall,
        781: ascii_arts.tornado,
        800: ascii_arts.clear_day,
        801: ascii_arts.clouds
    }

    for key, art in ascii_mapping.items():
        if isinstance(key, range):
            if weather_data[0][-1] in key:
                ascii_art = art
                break
        elif isinstance(key, int):
            if weather_data[0][-1] == key:
                ascii_art = art
                break

    for i in range(11):
        print(ascii_art[i] + f" {weather_data[0][i]}")


def display_weather_data_ascii_color(weather_data):
    os.system('clear')
    
    ascii_mapping = {
        range(200, 232): ascii_arts.thunder,
        range(300, 321): ascii_arts.dust,
        range(500, 531): ascii_arts.rain,
        range(600, 622): ascii_arts.snow,
        701: ascii_arts.dust,
        711: ascii_arts.smoke,
        721: ascii_arts.dust,
        731: ascii_arts.dust,
        741: ascii_arts.fog,
        751: ascii_arts.dust,
        761: ascii_arts.dust,
        762: ascii_arts.ash,
        771: ascii_arts.squall,
        781: ascii_arts.tornado,
        800: ascii_arts.clear_day,
        801: ascii_arts.clouds
    }

    for key, art in ascii_mapping.items():
        if isinstance(key, range):
            if weather_data[0][-1] in key:
                ascii_art = art
                break
        elif isinstance(key, int):
            if weather_data[0][-1] == key:
                ascii_art = art
                break

    weather_data = weather_data[1]
    
    r_print(Columns([Panel.fit("\n".join(ascii_art)), "\n".join(weather_data)]))


def display_weather_one_liner(weather_data):
    os.system('clear')

    print(f"Location: {weather_data[0][1]} | Temp: {weather_data[0][2]} | Humidity: {weather_data[0][6]} | Pressure: {weather_data[0][9]} | {weather_data[0][8]}")


def display_weather(weather_data):
    os.system('clear')

    print(f"Weather data for {weather_data[0][1]}")
    print(f" {'-' * (len('Weather data for') + len({weather_data[0][1]}) - 2)} ")
    print(f"Temperature:          {weather_data[0][2]}")
    print(f"Humidity:             {weather_data[0][6]}")
    print(f"Min Temperature:      {weather_data[0][4]}")
    print(f"Max Temperature:      {weather_data[0][5]}")
    print(f"Condition:            {weather_data[0][8]}")
    print(f"Pressure:             {weather_data[0][9]}")