import pandas as pd
import numpy as np 
import requests
import json
import openpyxl
from soil_analysis_database import DatabaseCRUDOperations

# Weather bit endpoints - https://api.weatherbit.io/v2.0/current?lat=35.7796&lon=-78.6382&key=API_KEY&include=minutely
weatherbit_api_key = "fdcf917e61644e42b23bda85da0c0309"
# OpenWeather endpoint - https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid={API key}
openweather_api_key = "464f061d35c8e41f2c783f8262dc42b1"

#Weather bit base endpoint
weatherbit_endpoint = r"https://api.weatherbit.io/v2.0/current?"
#Open weather base endpoint
openweather_endpoint = r"https://api.openweathermap.org/data/2.5/weather?"

'''
Soil Moisture = (0.408*delta*(Rn-G) + gamma*[900/(T+273)]*u2(es-ea))/(delta+gamma(1+0.34*u2))

u2 = Wind Speed at 2m height {WB}

es = Saturation Vapour Pressure
ea = Actual Vapour Pressure
es-ea = Saturation Vapour Pressure deficit

T = Mean daily temperature at 2m height {WB}
Td = Dew point temperature {WB}

es = 6.11 * 10^(7.5*Td/(237.5+Td))
ea = 6.11 * 10^(7.5*T/(237.5+T))

delta = (4098*es)/(T+237.5)^2
gamma =  0.066 kPa/°C 
G = 0.14*Rn

Rn = (1-alpha)*Rs - G
1.14*Rn = (1-alpha)*Rs
Rn = (1-alpha)*Rs/(1.14)

Rs = Solar Radiation {WB}
alpha = Lies in [0,1] depending on nature of land. 
        If snow {WB} > 10: alpha = 0.8
        If 5 < snow < 10: alpha = 0.5
        If 0 <= snow <= 5: alpha = 0.15
'''
def transform_input_data(input_data:list)->str:
        '''
        The objective of this function is to modify the input data to insert into the database.
        '''
        fields_str = "("
        for item in input_data:
                if isinstance(item,str):
                        fields_str+="'"+item+"',"
                else:
                        fields_str+=str(item)+","
        fields_str = fields_str[:-1]+")"

        return fields_str

def calculate_inputs(temperature,dew_pt_temp,dni,dhi,ghi,solar_radiation)->list:
        '''
        This method is to compute SaturationVapourPressure,ActualVapourPressure,SaturationVapourPressureDeficit,delta
        '''

        print("Calculating all the required input fields")
        es_exp = 7.5*dew_pt_temp/(237.5+dew_pt_temp)
        ea_exp = 7.5*temperature/(237.5+temperature)

        es = np.round(6.11*pow(10,es_exp),4)
        ea = np.round(6.11*pow(10,ea_exp),4)

        saturation_vapour_pressure_deficit = np.round(es-ea,4)
        delta = np.round((4098*es)/(pow(temperature+237.5,2)),4)

        if ghi==0:
                alpha = 1 
        else:
                alpha = np.round(1 - ((dni+dhi)/ghi),4)

        net_solar_raditation = np.round((1-alpha)*solar_radiation/(1.14),4)
        soil_heat_flux_density = 0.14*net_solar_raditation

        return [es,ea,saturation_vapour_pressure_deficit,delta,alpha,solar_radiation,net_solar_raditation,soil_heat_flux_density]

def get_required_fields(weatherbit_data: dict, openweather_data: dict)->list:
        '''
        The objective of this function is to retrieve the required fields for inserting into the database.
        '''
        print("Retrieving data from weatherbit API")
        weatherbit_data = weatherbit_data['data'][0]
        date = weatherbit_data['datetime']
        dew_pt_temp = weatherbit_data['dewpt']
        temp = weatherbit_data['temp']
        #snow = weatherbit_data['snow']
        solar_radiation= weatherbit_data['solar_rad']
        wind_speed = weatherbit_data['wind_spd']
        dhi = weatherbit_data['dhi']
        dni = weatherbit_data['dni']
        ghi = weatherbit_data['ghi']

        print("Retrieving data from Openweather API")
        #pressure = openweather_data['main']['pressure']
        #humidity = openweather_data['main']['humidity']
        temperature_in_kelvin = openweather_data['main']['temp']
        wind_speed_ow = openweather_data['wind']['speed']

        temp_in_celsius = temperature_in_kelvin - 273.15
        temperature = np.round((temp + temp_in_celsius)/2,4)

        wind_speed = np.round((wind_speed + wind_speed_ow)/2,4)

        print("Data retrieved both APIs successfully")
        calculated_inputs = calculate_inputs(temperature,dew_pt_temp,dni,dhi,ghi,solar_radiation)

        print(calculate_inputs)

        return [date,wind_speed,temperature,dew_pt_temp]+calculated_inputs

def make_API_request(latitude,longitude):
        '''
        The objective of this function is to use GET requests to retrieve API data from weatherbit and openweather.
        '''
        weatherbit_request = f"lat={latitude}&lon={longitude}&key="+weatherbit_api_key+"&include=minutely"
        weatherbit_api_request = requests.get(weatherbit_endpoint+weatherbit_request)

        openweather_request = f"lat={latitude}&lon={longitude}&appid="+openweather_api_key
        openweather_api_request = requests.get(openweather_endpoint+openweather_request)

        weatherbit_json = json.loads(weatherbit_api_request.text)
        openweather_json = json.loads(openweather_api_request.text)

        return (weatherbit_json, openweather_json)

geospatial_df = pd.read_excel(".\Inputs\City_Geospatial_Data_Test.xlsx")
data_to_insert = ""
for index,row in geospatial_df.iterrows():
      latitude = row[1]
      longitude = row[2]
      city = row[0]
      print(f'Retrieving data for {city}')
      weatherbit_data, openweather_data = make_API_request(latitude,longitude)
      input_data = get_required_fields(weatherbit_data, openweather_data)
      input_data.insert(0,city)
      data_to_insert += transform_input_data(input_data)+", "

data_to_insert = data_to_insert.rstrip(", ")

database_path = r"Database\\soil_analysis.db"
soil_db_obj = DatabaseCRUDOperations(database_path)

insert_query = "INSERT INTO Soil_Moisture (City,Date,Windspeed,Temperature_Celsius,DewPointTemperature_Celsius,SaturationVapourPressure,ActualVapourPressure,SaturationVapourPressureDeficit,Delta,Alpha,SolarRadiation,NetSolarRadiation,SoilHeatFluxDensity) VALUES "+data_to_insert

#insert_query = "INSERT INTO Soil_Moisture VALUES ('SFO', '2024-01-31 19:29:00', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11);"
soil_db_obj.insert_records(insert_query)

soil_db_obj.close_connection()

results = soil_db_obj.read_table("Select * FROM Soil_Moisture")    
for row in results:
    print(row)

############################################################################################################################

geospatial_df_test = pd.read_excel(".\Inputs\City_Geospatial_Data_Test.xlsx")
openweather_endpoint = r"https://api.openweathermap.org/data/2.5/weather?"
openweather_api_key = "464f061d35c8e41f2c783f8262dc42b1"

for index,row in geospatial_df_test.iterrows():
        latitude = row[1]
        longitude = row[2]
        city = row[0]
        print(f'Retrieving data for {city}')
        test_openweather = "lat={latitude}&lon={longitude}&appid="+openweather_api_key
        openweather_api_request = requests.get(openweather_endpoint+test_openweather)
        openweather_data = json.loads(openweather_api_request.text)
        print(openweather_data)	

############################################################################################################################
'''
items = ['apple',1,2,3,'orange']

fields = "("
for item in items:
        if isinstance(item,str):
              fields+="'"+item+"',"
        else:
              fields+=str(item)+","
fields = fields[:-1]+")"

for item in items:
       if item.type=="__str__":
              print("yes")

test_weatherbit = "lat=40.8620&lon=-74.5444&key="+weatherbit_api_key+"&include=minutely"
test_openweather = "lat=40.8620&lon=-74.5444&appid="+openweather_api_key

#Get latitude and longitude for each place and call API
weatherbit_api_request = requests.get(weatherbit_endpoint+test_weatherbit)
openweather_api_request = requests.get(openweather_endpoint+test_openweather)
weatherbit_data = json.loads(weatherbit_api_request.text)
openweather_data = json.loads(openweather_api_request.text)

print(weatherbit_api_request.text)
print(openweather_api_request.text)

print(openweather_data)

weatherbit_data = json.loads(weatherbit_api_request.text)
weatherbit_data = weatherbit_data['data'][0]

openweather_data = json.loads(openweather_api_request.text)

temperature = openweather_data['main']['temp']
pressure = openweather_data['main']['pressure']
humidity = openweather_data['main']['humidity']
wind_speed = openweather_data['wind']['speed']

test_str = ""
for i in range(5):
       test_str += "ABC"+",\n"
print(test_str[:-1])

latitude, longitude = 41.2956,-82.1512

test_weatherbit = f"lat={latitude}&lon={longitude}&key="+weatherbit_api_key+"&include=minutely"
test_openweather = "lat={latitude}&lon={longitude}&appid="+openweather_api_key

weatherbit_api_request = requests.get(weatherbit_endpoint+test_weatherbit)
openweather_api_request = requests.get(openweather_endpoint+test_openweather)
weatherbit_data = json.loads(weatherbit_api_request.text)
openweather_data = json.loads(openweather_api_request.text)

print(openweather_data)	
'''
latitude, longitude = 41.2956,-82.1512

latitude, longitude = 44.34, 10.99

test_weatherbit = f"lat={latitude}&lon={longitude}&key="+weatherbit_api_key+"&include=minutely"
test_openweather = "lat={latitude}&lon={longitude}&appid="+openweather_api_key

weatherbit_api_request = requests.get(weatherbit_endpoint+test_weatherbit)
openweather_api_request = requests.get(openweather_endpoint+test_openweather)

weatherbit_data = json.loads(weatherbit_api_request.text)
openweather_data = json.loads(openweather_api_request.text)

print(openweather_data)	