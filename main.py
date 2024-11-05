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


sp = pandas.read.csv("Student_Performance_Data.csv")


def create_database():
    curs.execute("CREATE DATABASE data")

    
    
    
conn.database = ("data")




conn.close()
sys.exit()