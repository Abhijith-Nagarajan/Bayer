import pandas as pd
import numpy as np 
import requests
import json
from soil_analysis_database import DatabaseCRUDOperations

# Weather bit endpoints - https://api.weatherbit.io/v2.0/current?lat=35.7796&lon=-78.6382&key=API_KEY&include=minutely
weatherbit_api_key = "fdcf917e61644e42b23bda85da0c0309"
# OpenWeather endpoint - https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid={API key}
openweather_api_key = "464f061d35c8e41f2c783f8262dc42b1"

weatherbit_endpoint = r"https://api.weatherbit.io/v2.0/current?"
openweather_endpoint = r"https://api.openweathermap.org/data/2.5/weather?"

test_weatherbit = "lat=40.8620&lon=-74.5444&key="+weatherbit_api_key+"&include=minutely"
test_openweather = "lat=40.8620&lon=-74.5444&appid="+openweather_api_key

# Get latitude and longitude for each place and call API

weatherbit_api_request = requests.get(weatherbit_endpoint+test_weatherbit)
openweather_api_request = requests.get(openweather_endpoint+test_openweather)

weatherbit_data = json.loads(weatherbit_api_request.text)
openweather_data = json.loads(openweather_api_request.text)

'''
Soil Moisture = (0.408*delta*(Rn-G) + gamma*[900/(T+273)]*u2(es-ea))/(delta+gamma(1+0.34*u2))

u2 = Wind Speed at 2m height 

es = Saturation Vapour Pressure
ea = Actual Vapour Pressure
es-ea = Saturation Vapour Pressure deficit

T = Mean daily temperature at 2m height
Td = Dew point temperature

es = 6.11 * 10^(7.5*Td/(237.5+Td))
ea = 6.11 * 10^(7.5*T/(237.5+T))

delta = (4098*es)/(T+237.5)^2
gamma =  0.066 kPa/°C 
G = 0.14*Rn
Rn = (1-alpha)*Rs - G
1.14*Rn = (1-alpha)*Rs
Rn = (1-alpha)*Rs/(1.14)
Rs = Solar Radiation
alpha = Lies in [0,1] depending on nature of land. 
        If snow > 10: alpha = 0.8
        If 5 < snow < 10: alpha = 0.5
        If 0 <= snow <= 5: alpha = 0.15
'''
print(weatherbit_data)

print(openweather_data)

weatherbit_data['data'][0]['dewpt']
print(type(openweather_api_request.text))

database_path = r"Database\\soil_analysis.db"

soil_db_obj = DatabaseCRUDOperations(database_path)

insert_query = "INSERT INTO Soil_Moisture VALUES ('SFO', '2024-01-31 19:29:00', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11);"
soil_db_obj.insert_records(insert_query)

results = soil_db_obj.read_table("Select * FROM Soil_Moisture")    

for row in results:
    print(row)


