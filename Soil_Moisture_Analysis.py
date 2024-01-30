import pandas as pd
import numpy as np 
import requests


# Weather bit endpoints - https://api.weatherbit.io/v2.0/current?lat=35.7796&lon=-78.6382&key=API_KEY&include=minutely
weatherbit_api_key = "fdcf917e61644e42b23bda85da0c0309"
# OpenWeather endpoint - https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}
openweather_api_key = "464f061d35c8e41f2c783f8262dc42b1"

weatherbit_endpoint = r"https://api.weatherbit.io/v2.0/current?"
# Get latitude and longitude for each place
