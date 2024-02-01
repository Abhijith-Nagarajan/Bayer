import os
import pandas as pd

base_path = r"Inputs\PRISM"
state_df = pd.DataFrame()

#temp_df = pd.read_csv("E:\Bayer\Inputs\PRISM\AvonLake_OH_PRISM.csv")

# Link to code - https://gist.github.com/sfirrin/fd01d87f022d80e98c37a045c14109fe
states_to_regions = {
    'Washington': 'West', 'Oregon': 'West', 'California': 'West', 'Nevada': 'West',
    'Idaho': 'West', 'Montana': 'West', 'Wyoming': 'West', 'Utah': 'West',
    'Colorado': 'West', 'Alaska': 'West', 'Hawaii': 'West', 'Maine': 'Northeast',
    'Vermont': 'Northeast', 'New York': 'Northeast', 'New Hampshire': 'Northeast',
    'Massachusetts': 'Northeast', 'Rhode Island': 'Northeast', 'Connecticut': 'Northeast',
    'New Jersey': 'Northeast', 'Pennsylvania': 'Northeast', 'North Dakota': 'Midwest',
    'South Dakota': 'Midwest', 'Nebraska': 'Midwest', 'Kansas': 'Midwest',
    'Minnesota': 'Midwest', 'Iowa': 'Midwest', 'Missouri': 'Midwest', 'Wisconsin': 'Midwest',
    'Illinois': 'Midwest', 'Michigan': 'Midwest', 'Indiana': 'Midwest', 'Ohio': 'Midwest',
    'West Virginia': 'South', 'District of Columbia': 'South', 'Maryland': 'South',
    'Virginia': 'South', 'Kentucky': 'South', 'Tennessee': 'South', 'North Carolina': 'South',
    'Mississippi': 'South', 'Arkansas': 'South', 'Louisiana': 'South', 'Alabama': 'South',
    'Georgia': 'South', 'South Carolina': 'South', 'Florida': 'South', 'Delaware': 'South',
    'Arizona': 'Southwest', 'New Mexico': 'Southwest', 'Oklahoma': 'Southwest',
    'Texas': 'Southwest'}

# Link to code - https://gist.github.com/rogerallen/1583593
us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}

abbrev_to_us_state = dict(map(reversed, us_state_to_abbrev.items()))
required_cols = ['Date','ppt (inches)','tmin (degrees F)','tmean (degrees F)','tmax (degrees F)',
                 'tdmean (degrees F)','vpdmin (hPa)','vpdmax (hPa)']

for file in os.listdir(base_path):
    #print(file)
    file_path = os.path.join(base_path,file)
    #print(file_path)
    temp_df = pd.read_csv(file_path)
    
    try:
        if (len(temp_df.columns)!=len(required_cols)) | (list(temp_df.columns)!=required_cols):
            raise Exception("Incorrect columns exception")
    except Exception as e:
        print("Error in file: ",file,"\nMessage:",e)

    file_name = file.split("_PRISM.csv")[0]
    city, state_abb = file_name.split("_")[0], file_name.split("_")[1]
    state = abbrev_to_us_state[state_abb]
    region = states_to_regions[state]
    #print(city,":",state_abb)
    temp_df['City'] = city
    temp_df['State_Abb'] = state_abb
    temp_df['State'] = state
    temp_df['Region'] = region
    state_df = pd.concat([state_df,temp_df],axis=0)

state_df['Date'] = pd.to_datetime(state_df['Date'])
state_df['Day']  = state_df['Date'].dt.day
state_df['Month'] = state_df['Date'].dt.month
state_df['Year'] = state_df['Date'].dt.year

renamed_cols = ['Precipitation(Inches)','Min_Temperature(F)','Mean_Temperature(F)','Max_Temperature(F)','Mean_Dewpoint_Temp(F)',
                'Min_VPD(hPa)','Max_VPD(hPa)']

required_cols.remove('Date')
cols = dict(zip(required_cols,renamed_cols))

state_df = state_df.rename(columns=cols)

def month_season_mapping(month:int)-> str:
    if month in [1,2,12]:
        return 'Winter'
    elif month in [3,4,5]:
        return 'Spring'
    elif month in [6,7,8]:
        return 'Summer'
    return 'Fall'

state_df = state_df[state_df.Year!=2024]
state_df['Precipitation(mm)'] = state_df['Precipitation(Inches)']*25.4 
state_df['Season'] = state_df['Month'].apply(lambda row: month_season_mapping(row))
state_df = state_df.set_index('Date')

state_df.to_csv(r"Inputs\TemperatureAnalysis.csv")


    
