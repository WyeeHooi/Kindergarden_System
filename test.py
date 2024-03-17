import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry  # Import DateEntry from tkcalendar module
from tkinter import messagebox

def save_student_data(entry_fields, profile_pic_var, right_frame):
    # Get values from entry fields
    id = entry_fields["id"].get()
    name = entry_fields["name"].get()
    age = entry_fields["age"].get()
    contact = entry_fields["contact"].get()
    address = entry_fields["address"].get()
    enroll_date = entry_fields["enrollment_date"].get()  # Correct key
    year = entry_fields["year"].get()  # Correct key

    # Get profile picture path
    Profile_pic = profile_pic_var.get()

    # Insert data into the database
    # Assuming the database connection and cursor are already defined
    query = "INSERT INTO student (id, name, age, contact, address, enroll_date, year, profile_pic) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (id, name, age, contact, address, enroll_date, year, Profile_pic))
    conn.commit()

    # Show success message
    messagebox.showinfo("Success", "Student data saved successfully.")

    # Refresh the treeview with updated data
    refresh_treetable(right_frame)

    # Clear entry fields after saving data
    for entry in entry_fields.values():
        entry.delete(0, tk.END)

def propagate_selected_row(event):
    # Get the selected item
    selected_item = student_treeview.selection()
    if selected_item:
        # Get the values of the selected row
        values = student_treeview.item(selected_item, "values")
        # Update the entry fields with the selected row's values
        for label, value in zip(student_labels, values):
            entry_fields[label.lower().replace(" ", "_")].delete(0, tk.END)
            entry_fields[label.lower().replace(" ", "_")].insert(0, value)
        # Disable the ADD and CLEAR buttons, and enable the EDIT and DELETE buttons
        add_button['state'] = 'disabled'
        edit_button['state'] = 'enabled'
        delete_button['state'] = 'enabled'
        clear_btn['state'] = 'disabled'

# Create the main window
window = tk.Tk()
window.title("Student Management System")

# Define student labels
student_labels = ["ID", "Name", "Age", "Contact", "Address", "Enrollment Date", "Year"]

# Create the left and right frames
left_frame = tk.Frame(window, bg='white')
left_frame.pack(side=tk.LEFT, fill=tk.Y)

right_frame = tk.Frame(window, bg='#F0E5F0')
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Create entry fields and profile picture selection button in the left frame
entry_fields = {}
for i, label in enumerate(student_labels, start=1):
    ttk.Label(left_frame, text=label).grid(row=i, column=0, padx=10, pady=5)
    if label != "Year" and label != "Enrollment Date":
        entry_fields[label.lower().replace(" ", "_")] = ttk.Entry(left_frame)
        entry_fields[label.lower().replace(" ", "_")].grid(row=i, column=1, padx=10, pady=5)
    elif label == "Year":
        # Create a dropdown menu for the 'Year' field
        year_combobox = ttk.Combobox(left_frame, values=["Year 1", "Year 2", "Year 3"], state="readonly")
        year_combobox.grid(row=i, column=1, padx=10, pady=5)
        entry_fields[label.lower().replace(" ", "_")] = year_combobox
    else:  # label == "Enrollment Date"
        # Create a DateEntry widget for selecting the date
        enrollment_date_entry = DateEntry(left_frame, date_pattern="yyyy-mm-dd")
        enrollment_date_entry.grid(row=i, column=1, padx=10, pady=5)
        entry_fields[label.lower().replace(" ", "_")] = enrollment_date_entry

# Profile pic selection button
profile_pic_var = tk.StringVar()
profile_pic_button = ttk.Button(left_frame, text="Select Profile Picture", command=lambda: select_profile_pic(profile_pic_var))
profile_pic_button.grid(row=len(student_labels) + 1, columnspan=2, padx=10, pady=5)

# Create the buttons at the bottom of the left frame
add_button = ttk.Button(left_frame, text="Add", command=lambda: save_student_data(entry_fields, profile_pic_var, right_frame))
add_button.grid(row=len(student_labels) + 2, columnspan=2, padx=10, pady=5)

edit_button = ttk.Button(left_frame, text="Edit", state="disabled")
edit_button.grid(row=len(student_labels) + 3, columnspan=2, padx=10, pady=5)

delete_button = ttk.Button(left_frame, text="Delete", state="disabled")
delete_button.grid(row=len(student_labels) + 4, columnspan=2, padx=10, pady=5)

clear_btn = ttk.Button(left_frame, text="Clear", state="disabled")
clear_btn.grid(row=len(student_labels) + 5, columnspan=2, padx=10, pady=5)

# Create the search entry and button in the right frame
search_entry = ttk.Entry(right_frame, width=30)
search_entry.grid(row=0, column=0, padx=10, pady=10)

search_button = ttk.Button(right_frame, text="Search")
search_button.grid(row=0, column=1, padx=10, pady=10)

# Create the student treeview in the right frame
student_treeview = ttk.Treeview(right_frame, columns=student_labels, show="headings")
student_treeview.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Bind the selection event to the propagate_selected_row function
student_treeview.bind("<<TreeviewSelect>>", propagate_selected_row)

# Run the main event loop
window.mainloop()