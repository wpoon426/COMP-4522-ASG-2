import mariadb
import pandas
import numpy
import sys
import csv



try:
    conn = mariadb.connect(
        user="user",
        password="",
        host="localhost",
    )
    print("Connected to Database")

except mariadb.Error as e:
    print(f"Error :(: {e}")
    sys.exit(1)

curs = conn.cursor()
conn.database = ("data")





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