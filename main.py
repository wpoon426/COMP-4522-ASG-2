import mariadb
import pandas
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy
import sys
import csv

# TO AVOID DUPLICATES DROP TABLES BEFORE RESTARTING PROGRAM



# Queries that show info that needs to be deleted
del_queries = [
    ("Select * FROM Performance WHERE Marks > 100 OR Marks < 0"),
    ("Select * FROM Performance WHERE Effort_Hours < 0"),
    ("Select * FROM Performance WHERE Student_ID IS NULL OR Semster_Name IS NULL OR Paper_ID IS NULL OR Paper_Name IS NULL OR Marks IS NULL OR Effort_Hours IS NULL")    
]
#Queries that will display exceptions and or delete improper data
sql_queries = [
    ("Select * FROM Department GROUP BY Department_ID HAVING COUNT(Department_ID) > 1"),
    ("Select * FROM Department GROUP BY Department_Name HAVING COUNT(Department_Name) > 1"),
    ("SELECT Department_ID, Department_Name, DOE FROM Department WHERE YEAR(STR_TO_DATE(DOE, '%m/%d/%Y')) < 1900"),# for the DOE >= 1900 but not sure how to do due to DOE being in reverse order and a string
    ("Select * FROM Department WHERE Department_ID IS NULL OR Department_Name IS NULL OR DOE IS NULL"),
    ("Select * FROM Students WHERE Department_Admission IS NULL"),
    ("Select Students.Department_Admission, Student_ID FROM Department,Students WHERE Students.Department_Admission NOT IN (SELECT Department.Department_ID FROM Department)"),
    ("DELETE FROM Performance WHERE Marks > 100 OR Marks < 0"),
    ("DELETE FROM Performance WHERE Effort_Hours < 0"),
    ("SELECT Student_ID, Paper_ID, COUNT(*) AS Duplicate_Count FROM Performance GROUP BY Student_ID, Paper_ID HAVING COUNT(*) > 1"),
    ("DELETE FROM Performance WHERE Student_ID IS NULL OR Semster_Name IS NULL OR Paper_ID IS NULL OR Paper_Name IS NULL OR Marks IS NULL OR Effort_Hours IS NULL")
]
# Drop all tables before re running to avoid duplicate data in each table.
try:
    #Connect to db
    conn = mariadb.connect(
        host="localhost",
        user="franklin", #change to your username before attempting to connect
        password="",
    )
    print("Connected to mariaDB")


   
    cursor = conn.cursor()
    cursor.execute("DROP DATABASE IF EXISTS data")
    cursor.execute("CREATE DATABASE IF NOT EXISTS data")
    conn.database = 'data'
    #get data from csv files 
    department = pandas.read_csv('data/Department_Information.csv')
    employee = pandas.read_csv('data/Employee_Information.csv')
    students = pandas.read_csv('data/Student_Counceling_Information.csv')
    performance = pandas.read_csv('data/Student_Performance_Data.csv')



    #creating sql tables for each csv file
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Department (
    Department_ID VARCHAR(100) PRIMARY KEY,
    Department_Name LONGTEXT,
    DOE VARCHAR(255)
        );
        """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Employee (
    Employee_ID VARCHAR(50) PRIMARY KEY,
    DOB VARCHAR(20),
    DOJ VARCHAR(20),
    Department_ID VARCHAR(100),
    FOREIGN KEY (Department_ID) REFERENCES Department(Department_ID)
        );
        """)
    
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Students (
    Student_ID VARCHAR(100),
    DOA VARCHAR(20),
    DOB VARCHAR(20),
    Department_Choices VARCHAR(50),
    Department_Admission VARCHAR(50),
    PRIMARY KEY (Student_ID, DOA, Department_Choices),
    FOREIGN KEY (Department_Choices) REFERENCES Department(Department_ID),
    FOREIGN KEY (Department_Admission) REFERENCES Department(Department_ID)
        );
        """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Performance (
    Student_ID VARCHAR(100),
    Semster_Name VARCHAR(100),
    Paper_ID VARCHAR(50),
    Paper_Name LONGTEXT,
    Marks INTEGER,
    Effort_Hours INTEGER,
    PRIMARY KEY (Student_ID, Paper_ID, Semster_Name),
    FOREIGN KEY (Student_ID) REFERENCES Students(Student_ID)
        );
        """)
    


    #inserting data from csv files into sql tables
    # try catch to find and remove Duplicate Primary keys
    try:
        for index, row in department.iterrows():
            cursor.execute("INSERT IGNORE INTO Department (Department_ID, Department_Name, DOE) VALUES (?,?,?)", (row.Department_ID, str(row.Department_Name), str(row.DOE) ))
            conn.commit()
    except mariadb.IntegrityError as er:
        if er.errno == 1062:
            print(f"Dupe Primary KEY: ", er)
            for index, row in department.iterrows():
                cursor.execute("INSERT IGNORE INTO Department (Department_ID, Department_Name, DOE) VALUES (?,?,?)", (row.Department_ID, str(row.Department_Name), str(row.DOE) ))
                conn.commit()

    for index, row in employee.iterrows():
        cursor.execute("INSERT IGNORE INTO Employee (Employee_ID, DOB, DOJ, Department_ID) values(?,?,?,?)", (row.Employee_ID, row.DOB, row.DOJ, row.Department_ID))
    conn.commit()

    for index, row in students.iterrows():
        cursor.execute("INSERT IGNORE INTO Students (Student_ID, DOA, DOB, Department_Choices, Department_Admission) values(?,?,?,?,?)", (row.Student_ID, row.DOA, row.DOB, str(row.Department_Choices), str(row.Department_Admission)))
    conn.commit()

    for index, row in performance.iterrows():
        cursor.execute("INSERT IGNORE INTO Performance (Student_ID, Semster_Name, Paper_ID, Paper_Name, Marks, Effort_Hours) values(?,?,?,?,?,?)", (row.Student_ID, row.Semster_Name, row.Paper_ID, str(row.Paper_Name), row.Marks, row.Effort_Hours))
    conn.commit()

    #function to show the exceptions or checks for improper/missing values
    #Removes bad data yet from Performance Table
    def Checks(querys,del_queries):
        index = 1
        for query in querys:
            if(query.split(' ')[0] == 'DELETE'):
                for q in del_queries:
                    cursor.execute(q)
                    result = cursor.fetchall()
                    if not result:# if query yeilds no results
                        index = index + 1
                        break
                    print("Check:",index)
                    print(f"The following records are being thrown as an Removed due to issues of Inconsistencys, Missing Values or improper Validity for Data needed for Analytics tasks: ",result, "\n")
                    index = index + 1
                cursor.execute(query)
                conn.commit()
                index = index + 1
            else:
                print("Check:",index)
                cursor.execute(query)
                result = cursor.fetchall()
                if not result:
                    print(f"The query Came up empty :(",result,"\n")
                else:
                    print(f"The following records are being thrown as an exception due to issues of Inconsistencys, Missing Values or improper Validity: ",result, "\n")
                index = index + 1
    
    Checks(sql_queries, del_queries)

    total_effort_by_semester = performance.groupby('Semster_Name')['Effort_Hours'].sum()
    print("Total Effort Hours by Semester:")
    print(total_effort_by_semester)


 
    cursor.close()
    sys.exit()
#Error Checking
except mariadb.IntegrityError as er:
    if er.errno == 1062:
        print(f"Dupe Primary KEY: ", er)
except mariadb.Error as e:
    print(f"Error :(: {e}")
