import sqlite3
from sqlite3 import Error

class DatabaseCRUDOperations:
    def __init__(self,database_path:str):
        self.db_path = database_path
        conn = None
        try:
            conn = sqlite3.connect(database_path)
        except Error as e:
            print("Error occurred while connecting to the database: ",e)

        self.db_connection = conn
        self.cursor = conn.cursor()
    
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
    
    def read_table(self,query:str)->sqlite3.Cursor:
        print("Retrieving records")
        retrieved_records = self.cursor.execute(query)
        return retrieved_records

    def insert_records(self,insert_query:str)->None:
        print("Inserting records")
        self.cursor.execute(insert_query)
        self.db_connection.commit()

    def update_records(self,update_query:str)->None:
        print("Updating records")
        self.cursor.execute(update_query)
        self.db_connection.commit()
    
    def delete_records(self,delete_query:str)->None:
        print("Deleting records")
        self.cursor.execute(delete_query)
        self.db_connection.commit()
    
    def close_connection(self)->None:
        print("Closing Database connection")
        self.db_connection.close()

'''
database_path = r"Database\\soil_analysis.db"

soil_db = DatabaseCRUDOperations(database_path)

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
insert_query = "INSERT INTO Soil_Moisture VALUES ('SFO', '2024-01-31 19:29:00', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11);"

soil_db.insert_records(insert_query)

results = soil_db.read_table("Select * FROM Soil_Moisture")    

for row in results:
    print(row)

soil_db.close_connection()
'''

        
    