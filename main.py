import mariadb
import pandas
import numpy
import sys
import csv



try:
    conn = mariadb.connect(
        host="localhost",
        user="user",
        password="",
    )
    curs = conn.cursor()
    print("Connected to Database")

except mariadb.Error as e:
    print(f"Error :(: {e}")


def load_data_to_db():
    employee = pandas.read_csv('data/Employee_Information')
    department = pandas.read_csv('data/Department_Information')



def create_database():
    curs.execute("""
CREATE TABLE IF NOT EXISTS Employee (
    Employee_ID VARCHAR(50),
    DOB VARCHAR(20),
    DOJ VARCHAR(20),
    Department_ID VARCHAR(50)
);
""")


        

    
    
    
conn.database = ("data")




conn.close()
sys.exit()