# %%
# This is Import/Connection/Loading
import mariadb
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Connect to the database
db = mariadb.connect(
    host="127.0.0.1",
    port=3306,
    user="fsnap",
    password="rosco",
    database="data"
)

# Function to load tables into DataFrames
def load_table_dataframe(table_name, conn):
    query = f"SELECT * FROM {table_name};"
    dataframe = pd.read_sql(query, conn)
    return dataframe

# Load tables into DataFrames
department_df = load_table_dataframe("Department", db)
students_df = load_table_dataframe("Students", db)
performance_df = load_table_dataframe("Performance", db)

# Display head of performance data to verify data
print("Student Performance:")
print(performance_df.head())


# %%
#Step 1: Defining the student IDs and initalizing an empty list to store predictions.
student_ids = ['SID20131151', 'SID20149500', 'SID20182516']
predictions = []

# %% [markdown]
# This step initalizes the list of student IDs we are interested in and an empty list where we will save predictions

# %%
#Step 2: Loop through each student and train a linear regression model on their data
for student_id in student_ids:
    #Filtering data for the specific students
    student_data = performance_df[performance_df['Student_ID'] == student_id]

    #checking to see if theres enough data to train the model aka more then 1 entry
    if len(student_data) > 1:
        #defining features (Effort_Hours) and target (marks) for model
        x = student_data[['Effort_Hours']]
        y = student_data['Marks']

        # Initialize and train the linear regression model
        model = LinearRegression()
        model.fit(x, y)

        #For each Student, we initialize and train a new linear regression model on that students specific data
        #This model allows us to make a personalized prediction based on each students effort hours

        #Step 3: predicting the scores for a 10-hour effort
        predicted_score = model.predict(np.array([[10]]))[0]
        
        #retrieving department information for the student
        department_info = students_df[students_df['Student_ID'] == student_id]['Department_Admission'].values[0]

        #Append prediction results to the list
        predictions.append({
            'Student_ID': student_id,
            'Predicted Score for 10hr Effort': round(predicted_score, 2),
            'Department': department_info
        })

        print(f"Processed Student ID: {student_id}")

        #After training, we can predict the score for a 10-hour effort specific to each student.
        #We also retrieve and record the student's department information for display.


    else:
        print(f"Not enough data to train model for Student ID: {student_id}")

# %% [markdown]
# For each student ID, we want to filter the performance data to isolate the records for the specific students. 
# This ensures that we are only analyzing the individual student data for our predictions.

# %%
#Step 4: Converting predictions list to DataFrame for easier display to user
predictions_df = pd.DataFrame(predictions)
print("\nPredicted Scores for 10 Hours of Effort:")
print(predictions_df)

#Display the predictions in a structured DataFrame, showing predicted scores for each student based on 10 hours of effort.



