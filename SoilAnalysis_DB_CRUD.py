import sqlite3
from sqlite3 import Error

print(sqlite3.sqlite_version)

class SoilAnalysisDatabase:
    def __init__(self,database_path:str):
        self.db_path = database_path
        conn = None
        try:
            conn = sqlite3.connect(database_path)
        except Error as e:
            print("Error occurred while connecting to the database: ",e)

        self.db_connection = conn
    
    def create_table(self,table_name:str,database_schema:str)->None:
        table_exists_check_query = "Create Table if not exists "+table_name+" "+database_schema
        self.db_connection.execute(table_exists_check_query)
        print("Table created. Validating the same.")
        validation_query = f"Select Count(*) as rows from {table_name}"
        validation_results = self.db_connection.execute(validation_query)
        try:
            if validation_results.rowcount==-1:
                print("Validation successful")
            else: 
                raise("Table not created successfully")
        except Exception as e:
            print("Received error while creating table. "+e)
            self.close_connection()
    
    def read_table(self,query:str):
        print("Retrieving records")
        retrieved_records = self.db_connection.execute(query)
        return retrieved_records

    def insert_records(insert_query:str)->None:
        print("Inserting records")

    def update_records(update_query:str)->None:
        print("Updating records")
    
    def delete_records(delete_query:str)->None:
        print("Deleting records")
    
    def close_connection(self)->None:
        print("Closing Database connection")
        self.db_connection.close()

database_path = r"Database\\soil_analysis.db"

soil_db = SoilAnalysisDatabase(database_path)

table_name = "Soil_Moisture"
table_schema = """
                (
                    City nvarchar(200),
                    Date datetime,
                    WindSpeed numeric,
                    "Temperature(C)" numeric,
                    "DewPointTemperature(C)" numeric,
                    SaturationVapourPressure numeric,
                    ActualVapourPressure numeric,
                    SaturationVapourPressureDeficit numeric,
                    Delta numeric,
                    Alpha numeric,
                    SolarRadiation numeric,
                    NetSolarRadiation numeric,
                    SoilHeatFluxDensity numeric
                );
                """

soil_db.create_table(table_name,table_schema)


    


        
    