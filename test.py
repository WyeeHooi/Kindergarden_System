import tkinter as tk
from tkinter import messagebox

from datetime import datetime
import pymysql
# Database connection
connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='tintots_kindergarden'
    )

cursor=connection.cursor()

# Dummy student data (assuming subj_student is a dictionary)
subj_student = {1001: "John", 1002: "Alice", 1003: "Bob"}

# Create the main window
root = tk.Tk()
root.title("Attendance Taking")

# Create labels for the column headers
tk.Label(root, text="No.").grid(row=0, column=0)
tk.Label(root, text="Student ID").grid(row=0, column=1)
tk.Label(root, text="Student Name").grid(row=0, column=2)
tk.Label(root, text="Attendance").grid(row=0, column=3)

# Store attendance data
attendance_data = {}

# Create a checkbox for each student
for i, (student_id, student_name) in enumerate(subj_student.items(), start=1):
    tk.Label(root, text=str(i)).grid(row=i, column=0)
    tk.Label(root, text=str(student_id)).grid(row=i, column=1)
    tk.Label(root, text=str(student_name)).grid(row=i, column=2)
    var = tk.BooleanVar()
    checkbox = tk.Checkbutton(root, variable=var)
    checkbox.grid(row=i, column=3)
    attendance_data[student_id] = var

# Function to submit attendance
def submit_attendance():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        for student_id, var in attendance_data.items():
            student_name = subj_student[student_id]  # Retrieve student name from subj_student dictionary
            attendance = 1 if var.get() else 0
            sql = "INSERT INTO attendance_record (subject, stud_id, student, time_recorded, attendance) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, ("math", student_id, student_name, current_time, attendance))
        connection.commit()  # Commit changes to the database
        messagebox.showinfo("Success", "Attendance recorded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Database error: {str(e)}")


# Create submit button
submit_button = tk.Button(root, text="Submit", command=submit_attendance)
submit_button.grid(row=len(subj_student) + 1, columnspan=4)

# Run the application
root.mainloop()
