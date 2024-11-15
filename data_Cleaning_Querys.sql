drop table Department, Employee, Performance, Students;

----------Department Table Check-----------
--Check 1 Dep_ID uniqueness
Select Department_ID,COUNT(Department_ID) FROM Department GROUP BY Department_ID;
--OR 
Select * FROM Department GROUP BY Department_ID HAVING COUNT(Department_ID) > 1; -- use this in project

--Check 2 Dep_Name uniqueness
Select Department_Name,COUNT(Department_ID) FROM Department GROUP BY Department_Name;
--OR
Select * FROM Department GROUP BY Department_Name HAVING COUNT(Department_Name) > 1; -- Use this in project
-- Check 3 DOE YEAR (Had to convert the format of the DOE date)
SELECT Department_ID, Department_Name, DOE FROM Department WHERE YEAR(STR_TO_DATE(DOE, '%m/%d/%Y')) < 1900;
-- Check 4 missing values 
Select * FROM Department WHERE Department_ID IS NULL OR Department_Name IS NULL OR DOE IS NUll; -- Use this in Project

----------Student Counceling Info Checks-------------
--Checks 1 dep admin missing info
Select * FROM Students WHERE Department_Admission IS NULL; -- use for asg
-- Checks 2 department ad exists
Select * FROM Students LEFT OUTER JOIN Department ON Students.Department_Admission = Department.Department_ID LIMIT 5 ;
Select Students.Department_Admission, Student_ID FROM Department,Students WHERE Students.Department_Admission NOT IN (SELECT Department.Department_ID FROM Department) -- not sure if works right but gets one where there is no dept admission listed


-----------Performance table Checks-------------
-- Check 1 Marks below 0 and above 100:
Select * FROM Performance WHERE Marks > 100 OR Marks < 0;
-- Delete after reporting
DELETE FROM Performance WHERE Marks > 100 OR Marks < 0;

--Check 2 Negative Hours
Select * FROM Performance WHERE Effort_Hours < 0;
--Delect after Reporting
DELETE FROM Performance WHERE Effort_Hours < 0;

-- Check 3 (Pretty sure htis is correct although it comes back up as nothing)
SELECT Student_ID, Paper_ID, COUNT(*) AS Duplicate_Count FROM Performance GROUP BY Student_ID, Paper_ID HAVING COUNT(*) > 1;

-- Check 4 Missing Values 
Select * FROM Performance WHERE Student_ID IS NULL OR Semster_Name IS NULL OR Paper_ID IS NULL OR Paper_Name IS NULL OR Marks IS NULL OR Effort_Hours IS NULL;
--Delete after reporting
DELETE FROM Performance WHERE Student_ID IS NULL OR Semster_Name IS NULL OR Paper_ID IS NULL OR Paper_Name IS NULL OR Marks IS NULL OR Effort_Hours IS NULL;



