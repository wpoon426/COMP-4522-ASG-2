import mariadb
import pandas
import numpy
import sys
import csv


try:
    conn = mariadb.connect(
        host="localhost",
        user="zaarifsardar",
        password="",

    )
    print("Connected to mariaDB")
   
    cursor = conn.cursor()
    conn.database = 'data'

    employee = pandas.read_csv('data/Employee_Information.csv')
    print(employee)
   

    for index, row in employee.iterrows():
        cursor.execute("INSERT INTO Employee (Employee_ID, DOB, DOJ, Department_ID) values(?,?,?,?)", (row.Employee_ID, row.DOB, row.DOJ, row.Department_ID))
    conn.commit()
    cursor.close()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Employee (
    Employee_ID VARCHAR(50),
    DOB VARCHAR(20),
    DOJ VARCHAR(20),
    Department_ID VARCHAR(50)
);
""")
    cursor 
    



except mariadb.Error as e:
    print(f"Error :(: {e}")

cursor = conn.cursor()


def load_data_to_db():
    employee = pandas.read_csv('data/Employee_Information')
    department = pandas.read_csv('data/Department_Information')

    print(employee)


def create_database():
    cursor.execute("""
CREATE TABLE IF NOT EXISTS Employee (
    Employee_ID VARCHAR(50),
    DOB VARCHAR(20),
    DOJ VARCHAR(20),
    Department_ID VARCHAR(50)
);
""")


        

    
    





sys.exit()