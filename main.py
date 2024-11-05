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



def create_database():
    curs.execute("CREATE DATABASE data")


def load_data_to_db():
    file=('data/Employee_Information.csv')
    csv_data = csv.reader(file)
    for row in csv_data:
        print(row)
        

    
    
    
conn.database = ("data")




conn.close()
sys.exit()