import mariadb
import pandas
import numpy
import sys
import csv


try:
    #Connect to db
    conn = mariadb.connect(
        host="localhost",
        user="zaarifsardar", #change to your username before attempting to connect
        password="",


    )
    print("Connected to mariaDB")
   
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS data")
    conn.database = 'data'
    #get data from csv files 
    employee = pandas.read_csv('data/Employee_Information.csv')
    department = pandas.read_csv('data/Department_Information.csv')
    students = pandas.read_csv('data/Student_Counceling_Information.csv')
    performance = pandas.read_csv('data/Student_Performance_Data.csv')

    #creating sql tables for each csv file
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Employee (
    Employee_ID VARCHAR(50) PRIMARY KEY,
    DOB VARCHAR(20),
    DOJ VARCHAR(20),
    Department_ID VARCHAR(50)
        );
        """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Department (
    Department_ID VARCHAR(100) PRIMARY KEY,
    Department_Name LONGTEXT,
    DOE VARCHAR(5000)
        );
        """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Students (
    Student_ID VARCHAR(100),
    DOA VARCHAR(20),
    DOB VARCHAR(20),
    Department_Choices LONGTEXT,
    Department_Admission LONGTEXT
        );
        """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Performance (
    Student_ID VARCHAR(100),
    Semster_Name VARCHAR(100),
    Paper_ID VARCHAR(50),
    Paper_Name LONGTEXT,
    Marks INTEGER,
    Effort_Hours INTEGER
        );
        """)
    


    #inserting data from csv files into sql tables
    for index, row in employee.iterrows():
        cursor.execute("INSERT INTO Employee (Employee_ID, DOB, DOJ, Department_ID) values(?,?,?,?)", (row.Employee_ID, row.DOB, row.DOJ, row.Department_ID))
    conn.commit()


    for index, row in department.iterrows():
        cursor.execute("INSERT IGNORE INTO Department (Department_ID, Department_Name, DOE) VALUES (?,?,?)", (row.Department_ID, str(row.Department_Name), row.DOE))
    
    conn.commit()


    for index, row in students.iterrows():
        cursor.execute("INSERT INTO Students (Student_ID, DOA, DOB, Department_Choices, Department_Admission) values(?,?,?,?,?)", (row.Student_ID, row.DOA, row.DOB, str(row.Department_Choices), str(row.Department_Admission)))
    conn.commit()

    for index, row in performance.iterrows():
        cursor.execute("INSERT INTO Performance (Student_ID, Semster_Name, Paper_ID, Paper_Name, Marks, Effort_Hours) values(?,?,?,?,?, ?)", (row.Student_ID, row.Semster_Name, row.Paper_ID, str(row.Paper_Name), row.Marks, row.Effort_Hours))
    conn.commit()



    cursor.close()
    sys.exit()



except mariadb.Error as e:
    print(f"Error :(: {e}")
