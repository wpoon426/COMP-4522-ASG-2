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



def create_database():
    curs.execute("CREATE DATABASE data")

    
    
    
conn.database = ("data")




conn.close()
sys.exit()