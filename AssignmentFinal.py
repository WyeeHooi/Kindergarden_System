from tkinter import ttk, simpledialog
from tkinter import messagebox
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
import csv
import pymysql
from datetime import datetime




font = 'Lato'


def db_connect():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='tintots_kindergarden'
        )
        return conn
    except pymysql.Error as e:
        print("Error connecting to MySQL database:", e)
        messagebox.showerror("Error", "Failed to connect to database.")


def open_admin_login():
    global admin_login_frame
    admin_login_frame = tk.Frame(window)
    admin_login_frame.pack()
    main_buttons_frame.destroy()

    # Create username and password labels and entry widgets
    admin_username_label = ttk.Label(admin_login_frame, text="Username:", style="CustomLabel.TLabel")
    admin_username_label.pack()
    admin_username_entry = ttk.Entry(admin_login_frame, width=40, font=('Arial', 14))
    admin_username_entry.pack()

    admin_password_label = ttk.Label(admin_login_frame, text="Password:", style="CustomLabel.TLabel")
    admin_password_label.pack()
    admin_password_entry = ttk.Entry(admin_login_frame, show="*", width=40, font=('Arial', 14))
    admin_password_entry.pack(expand=True)

    # Create the login button
    admin_login_button = ttk.Button(admin_login_frame, text="Login",
                                    command=lambda: admin_authenticate(window, admin_username_entry,
                                                                       admin_password_entry),
                                    style="aactiveBtn.TButton", width=40)
    admin_login_button.pack(pady=10)


def staff_login():
    # Hide the main buttons frame
    main_buttons_frame.pack_forget()

    # Show the staff login frame
    staff_login_frame.pack(pady=150)


def admin_authenticate(parent_widget, admin_username_entry, admin_password_entry):
    # Get username and password
    username = admin_username_entry.get()
    password = admin_password_entry.get()

    # Check if ID is an 8-digit integer
    if len(username) != 8 or not username.isdigit():
        messagebox.showerror("Admin Login", "Invalid username format. Please enter an 8-digit integer.")
        return

    # Authenticate using database
    conn = pymysql.connect(host='localhost', user='root', password='', database='tintots_kindergarden')
    if conn:
        try:
            cursor = conn.cursor()
            # Fetch admin details from the database
            query = "SELECT * FROM staff WHERE id = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            if result:
                messagebox.showinfo("Admin Login", "Admin login successful!")
                # Proceed after successful admin login
                admin_login_frame.destroy()
                show_main_interface(parent_widget, result,
                                    action_frame)  # Pass the parent widget, user details, and action frame
            else:
                messagebox.showerror("Admin Login", "Invalid username or password.")
        except pymysql.Error as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")
        finally:
            conn.close()
    else:
        messagebox.showerror("Error", "Failed to connect to database.")


def staff_authenticate():
    username = staff_username_entry.get()
    password = staff_password_entry.get()

    if not (8 <= len(username) <= 10) or not username.isdigit():
        messagebox.showerror("Staff Login", "Invalid username, you may not an admin try to login as a staff")
        return

    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='tintots_kindergarden'
    )
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM staff WHERE id = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                import staff
                # messagebox.showinfo("Staff Login", "Staff login successful!")
                # Pass user ID as a list containing the username converted to an integer
                staff_login_frame.destroy()
                window.destroy()
                user_id = int(username)
                staff.initiate(user_id)

            else:
                messagebox.showerror("Staff Login", "Invalid username or password.")
        except pymysql.Error as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")
        finally:
            conn.close()
    else:
        messagebox.showerror("Error", "Failed to connect to database.")


def create_main_interface(parent_widget, action_frame, user):
    def on_window_configure(event):
        Frame_buttonNav.place(x=0, y=0, width=parent_widget.winfo_width(),
                              height=parent_widget.winfo_height() * 0.1)
        for frame in action_frame:
            frame.place(x=0, y=parent_widget.winfo_height() * 0.1, width=parent_widget.winfo_width(),
                        height=parent_widget.winfo_height() * 0.9)

    parent_widget.bind("<Configure>", on_window_configure)
    Frame_buttonNav = tk.Frame(parent_widget, bd=5, relief=tk.FLAT, bg="#F0E5F0")

    profile_button = ttk.Button(Frame_buttonNav, text="Profile",
                                command=lambda: show_main_interface(parent_widget, user, action_frame),
                                style='inactiveBtn.TButton', width=35)
    profile_button.grid(row=0, column=0, padx=22, pady=25)

    student_button = ttk.Button(Frame_buttonNav, text="Student Data",
                                command=lambda: [show_student_data(user, parent_widget, action_frame)],
                                style='inactiveBtn.TButton', width=35)
    student_button.grid(row=0, column=1, padx=22, pady=25)

    staff_button = ttk.Button(Frame_buttonNav, text="Staff Data",
                              command=lambda: [show_staff_data(user, parent_widget, action_frame)],
                              style='inactiveBtn.TButton', width=35)
    staff_button.grid(row=0, column=2, padx=22, pady=25)

    class_button = ttk.Button(Frame_buttonNav, text="Class Slot",
                              command=lambda: [show_class_slot(user, parent_widget, action_frame)],
                              style='inactiveBtn.TButton', width=35)
    class_button.grid(row=0, column=3, padx=22, pady=25)

    logout_button = ttk.Button(Frame_buttonNav, text="Logout", command=lambda: logout(window),
                               style='inactiveBtn.TButton', width=35)
    logout_button.grid(row=0, column=4, padx=22, pady=25)


def display_userPic(frame, width, height, user_id):
    conn = db_connect()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT profile_pic FROM staff WHERE id = %s;"
            cursor.execute(sql, (user_id,))
            # Fetch the result
            result = cursor.fetchone()
            if result:
                image_path = result[-1]  # Assuming the profile_pic column is the first column in the result
            else:
                # Handle case where no result is found
                image_path = None
    finally:
        # Close the connection
        conn.close()
        load_profilePic(frame, width, height, image_path)


def load_profilePic(frame, width, height, image_path):
    if image_path:
        # Load the image
        image = Image.open(image_path)
        # Resize the image
        image = image.resize((width, height), Image.LANCZOS)
        # Create a PhotoImage object
        photo = ImageTk.PhotoImage(image)
        # Create a Label to display the image
        label = ttk.Label(frame, image=photo)
        # Store a reference to the image to prevent it from being garbage collected
        label.image = photo
        # Place the Label in the frame
        label.grid(row=0, columnspan=2, padx=15, pady=15)
    else:
        print("No image path provided.")


def show_main_interface(parent_widget, user, action_frame):
    # Clear existing widgets from the parent frame
    for widget in parent_widget.winfo_children():
        widget.destroy()

    # Create a new frame to display user details
    user_details_frame = tk.Frame(parent_widget)
    user_details_frame.pack(pady=150)

    # Load profile picture
    user_id = user[0]
    display_userPic(user_details_frame, 180, 180, user_id)

    # Define labels for user details
    labels = ["ID", "Name", "Contact", "Password", "Age", "Address",
              "Email", "Qualification", "Position", "Department", "Salary"]

    user_details = {
        "ID": user[0],
        "Name": user[1],
        "Contact": user[2],
        "Password": user[3],
        "Age": user[4],
        "Address": user[5],
        "Email": user[6],
        "Qualification": user[7],
        "Position": user[8],
        "Department": user[9],
        "Salary": user[10]
    }

    # Display user details using labels
    for i, label in enumerate(labels, start=1):
        ttk.Label(user_details_frame, text=label, font=(font, 12, "normal")).grid(row=i, column=0, padx=10,
                                                                                    pady=5)
        ttk.Label(user_details_frame, text=user_details[label], font=(font, 12, "normal")).grid(row=i, column=1,
                                                                                                  padx=10, pady=5)

    # Create the main interface
    create_main_interface(parent_widget, action_frame, user)


def logout(window):
    window.destroy()
    window.deiconify()


# staff
def show_staff_data(user, parent_widget, action_frame):
    # Clear existing widgets from the parent frame
    for widget in parent_widget.winfo_children():
        widget.destroy()

    # Create a new frame for staff data
    action_frame = tk.Frame(parent_widget)
    action_frame.pack(fill=tk.BOTH, expand=True)

    # Left section for data entry
    left_frame = tk.Frame(action_frame)
    left_frame.pack(side=tk.LEFT, padx=150, pady=250, fill=tk.BOTH, expand=True)

    right_frame = tk.Frame(action_frame, height=800, width=1000)
    right_frame.pack(side=tk.RIGHT, padx=100, pady=50, fill=tk.BOTH, expand=True)

    # Labels for staff details entry
    staff_labels = ["ID", "Name", "Contact", "Password", "Age", "Address",
                    "Email", "Qualification", "Position", "Department", "Salary"]

    # Entry fields for staff details
    entry_fields = {}
    for i, label in enumerate(staff_labels):
        ttk.Label(left_frame, text=label, font=("Lato", 12, "normal")).grid(row=i, column=0, padx=10, pady=5)
        entry_fields[label.lower()] = ttk.Entry(left_frame)
        entry_fields[label.lower()].grid(row=i, column=1, padx=10, pady=5)

    # Profile pic selection
    profile_pic_var = tk.StringVar()
    profile_pic_label = ttk.Label(left_frame, text="Profile Picture", font=("Lato", 12, "normal"))
    profile_pic_label.grid(row=len(staff_labels), column=0, padx=5, pady=5)
    profile_pic_button = ttk.Button(left_frame, text="Select Profile Picture",
                                    command=lambda: select_profile_pic(profile_pic_var), style='Btn.TButton')
    profile_pic_button.grid(row=len(staff_labels), column=1, padx=5, pady=5)

    # Save button
    save_button = ttk.Button(left_frame, text="Save",
                             command=lambda: save_staff_data(entry_fields, profile_pic_var, right_frame),
                             style='Btn.TButton')
    save_button.grid(row=len(staff_labels) + 1, columnspan=2, padx=2, pady=2, sticky="we")

    # Clear fields button
    ttk.Button(left_frame, text="Clear Fields", command=lambda: clear_fields(entry_fields),
               style='Btn.TButton').grid(row=len(staff_labels) + 2, columnspan=2, padx=2, pady=2, sticky="we")
    # Delete button
    edit_button = ttk.Button(right_frame, text="Edit", command=lambda: edit_staff(staff_listbox),
                             style='Btn.TButton')
    edit_button.pack(side=tk.BOTTOM, padx=5, pady=5, fill=tk.X)

    delete_button = ttk.Button(right_frame, text="Delete", command=lambda: delete_staff_data(staff_listbox),
                               style='Btn.TButton')
    delete_button.pack(side=tk.BOTTOM, padx=5, pady=5, fill=tk.X)

    # Staff listbox
    staff_listbox = ttk.Treeview(right_frame, columns=staff_labels, show="headings", height=1000)
    for col in staff_labels:
        staff_listbox.column(col, width=850)
    staff_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=100)

    for label in staff_labels:
        staff_listbox.heading(label, text=label, anchor=tk.CENTER)
        staff_listbox.column(label, width=100)

    # Fetch data from the database and insert into the Treeview
    conn = db_connect()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM staff")
        rows = cursor.fetchall()
        for row in rows:
            staff_listbox.insert("", "end", values=row)

    create_main_interface(parent_widget, action_frame, user)


def delete_staff_data(staff_treeview):
    selected_item = staff_treeview.selection()
    if selected_item:
        # Retrieve the ID of the selected row
        selected_id = staff_treeview.item(selected_item, 'values')[0]  # Assuming the ID is the first column

        # Confirm deletion with the user
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this staff data?")
        if confirm:
            # Delete the selected data from the database
            conn = db_connect()
            if conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM staff WHERE id = %s", (selected_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Staff data deleted successfully.")
                # Refresh the staff list after deletion
                refresh_staff_listbox(staff_treeview)
    else:
        messagebox.showwarning("No Selection", "Please select a staff data to delete.")


def select_profile_pic(profile_pic_var):
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        profile_pic_var.set(file_path)


def save_staff_data(entries, profile_pic_var, staff_treeview):
    # Retrieve data from entry fields
    id = entries["id"].get()
    name = entries["name"].get()
    contact = entries["contact"].get()
    password = entries["password"].get()
    age = entries["age"].get()
    address = entries["address"].get()
    email = entries["email"].get()
    qualification = entries["qualification"].get()
    position = entries["position"].get()
    department = entries["department"].get()
    salary = entries["salary"].get()

    # Retrieve selected profile pic
    profile_pic = profile_pic_var.get()

    # Insert staff data into the database
    conn = db_connect()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO staff (ID, Name, Contact, Password, Age, Address, Email, Qualification, Position, Department, Salary, Profile_Pic) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (
            id, name, contact, password, age, address, email, qualification, position, department, salary,
            profile_pic))
        # Show confirmation message
        confirm = messagebox.askyesno("Confirm Saved", "Are you sure you want to save this staff data?")
        if confirm:
            conn.commit()
            messagebox.showinfo("Success", "Staff data saved successfully.")
            # Refresh the staff list after saving
            refresh_staff_listbox(staff_treeview)
            # Clear entry fields after saving
            for entry in entries.values():
                entry.delete(0, tk.END)


def edit_staff(staff_treeview):
    selected_items = staff_treeview.selection()
    if selected_items:
        # Get the selected staff member's data from the Treeview
        selected_staff = staff_treeview.item(selected_items[0])['values']
        # Open a new window or frame to display the selected staff member's details
        edit_window = tk.Toplevel(window)  # or tk.Tk() if you want a new window
        edit_window.title("Edit Staff Details")

        window_width = 1000
        window_height = 600

        # Add labels and entry fields to display staff details
        labels = ["ID", "Name", "Contact", "Password", "Age", "Address",
                  "Email", "Qualification", "Position", "Department", "Salary"]
        label_width = 100
        entry_width = 200
        row_height = 30
        label_entry_padx = 20
        label_entry_pady = 10
        start_y = (window_height - (len(labels) * row_height)) // 2  # Start Y position to center vertically

        entry_fields = {}  # Dictionary to hold entry fields

        for i, label_text in enumerate(labels):
            # Calculate X position to center horizontally
            label_x = (window_width - (2 * label_width + entry_width + 2 * label_entry_padx)) // 2
            entry_x = label_x + label_width + label_entry_padx

            # Calculate Y position
            y = start_y + i * row_height

            ttk.Label(edit_window, text=label_text).place(x=label_x, y=y, width=label_width, height=row_height)
            entry = ttk.Entry(edit_window)
            if i < len(selected_staff):
                entry.insert(0, selected_staff[i])  # Populate entry with staff data
            entry.place(x=entry_x, y=y, width=entry_width, height=row_height)
            entry_fields[label_text] = entry  # Append entry field to entry_fields dictionary

        # Add button to update staff details
        update_button = ttk.Button(edit_window, text="Update",
                                   command=lambda: update_staff(edit_window, selected_staff, entry_fields,
                                                                staff_treeview))
        update_button.place(x=(window_width - 100) // 2, y=start_y + len(labels) * row_height, width=100, height=30)


def update_staff(edit_window, selected_staff, entry_fields, staff_treeview):
    # Get the updated data from entry fields
    updated_data = [entry.get() for entry in entry_fields.values()]

    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='tintots_kindergarden'
    )
    # Connect to the database
    cursor = conn.cursor()

    try:
        # Construct the SQL query to update the staff details
        query = """
        UPDATE staff 
        SET Name = %s, Contact = %s, Password = %s, Age = %s, Address = %s,
            Email = %s, Qualification = %s, Position = %s, Department = %s, Salary = %s
        WHERE ID = %s
        """
        # Execute the query
        cursor.execute(query, (
            updated_data[1], updated_data[2], updated_data[3], updated_data[4],
            updated_data[5], updated_data[6], updated_data[7], updated_data[8],
            updated_data[9], updated_data[10], updated_data[0]
        ))
        # Commit changes to the database
        conn.commit()
        messagebox.showinfo("Success", "Staff data saved successfully.")
        # Close the edit window
        edit_window.destroy()
        # Refresh the staff listbox
        refresh_staff_listbox(staff_treeview)
    except pymysql.Error as e:
        messagebox.showinfo("Error", "Staff data saved unsuccessfully.")
        # Rollback changes in case of error
        conn.rollback()
    finally:
        # Close cursor and connection
        cursor.close()
        conn.close()


def refresh_staff_listbox(staff_treeview):
    staff_treeview.delete(*staff_treeview.get_children())
    # Clear existing data from the Treeview widget
    for child in staff_treeview.get_children():
        staff_treeview.delete(child)

    # Repopulate the Treeview widget with the latest data from the database
    conn = db_connect()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM staff")
        rows = cursor.fetchall()
        for row in rows:
            staff_treeview.insert('', 'end', values=row)
        conn.close()


# student
def show_student_data(user, parent_widget, action_frame):
    # Clear existing widgets from the parent frame
    for widget in parent_widget.winfo_children():
        widget.destroy()

    action_frame = tk.Frame(parent_widget)
    action_frame.pack(fill=tk.BOTH, expand=True)

    # Left frame for data entry
    left_frame = tk.Frame(action_frame)
    left_frame.pack(side=tk.LEFT, padx=150, pady=250, fill=tk.BOTH, expand=True)

    right_frame = tk.Frame(action_frame, height=800, width=1000)
    right_frame.pack(side=tk.RIGHT, padx=100, pady=50, fill=tk.BOTH, expand=True)

    # Entry fields labels
    student_labels = ["ID", "Name", "Age", "Contact", "Address", "Enrollment Date", "Year", "Emergency Contact"]

    # Entry fields
    entry_fields = {}
    for i, label in enumerate(student_labels):
        ttk.Label(left_frame, text=label, font=("Lato", 12, "normal")).grid(row=i, column=0, padx=10, pady=5)
        entry_fields[label.lower().replace(" ", "_")] = ttk.Entry(
            left_frame)  # Use lower case and replace space with underscore
        entry_fields[label.lower().replace(" ", "_")].grid(row=i, column=1, padx=10, pady=5)

    # Profile pic selection button
    profile_pic_var = tk.StringVar()
    profile_pic_label = ttk.Label(left_frame, text="Profile Picture", font=("Lato", 12, "normal"))
    profile_pic_label.grid(row=len(student_labels), column=0, padx=10, pady=5)
    profile_pic_button = ttk.Button(left_frame, text="Select Profile Picture",
                                    command=lambda: select_profile_pic(profile_pic_var), style='Btn.TButton')
    profile_pic_button.grid(row=len(student_labels), column=1, padx=10, pady=5)

    save_button = ttk.Button(left_frame, text="Save",
                             command=lambda: save_student_data(entry_fields, profile_pic_var, right_frame),
                             style='Btn.TButton')
    save_button.grid(row=len(student_labels) + 2, columnspan=2, padx=2, pady=2, sticky="we")

    # Clear fields button
    ttk.Button(left_frame, text="Clear Fields", command=lambda: clear_fields(entry_fields),
               style='Btn.TButton').grid(row=len(student_labels) + 3, columnspan=2, padx=2, pady=2, sticky="we")

    upload_button = ttk.Button(left_frame, text="Upload Student List", command=lambda: browse_file(right_frame),
                               style='Btn.TButton')
    upload_button.grid(row=len(student_labels) + 4, columnspan=2, padx=2, pady=2, sticky="we")

    update_image_button = ttk.Button(right_frame, text="Update Image", command=upload_image_popup,
                                     style='Btn.TButton')
    update_image_button.pack(side=tk.BOTTOM, padx=5, pady=5, fill=tk.X)

    edit_button = ttk.Button(right_frame, text="Edit", command=lambda: edit_student(student_treeview),
                             style='Btn.TButton')
    edit_button.pack(side=tk.BOTTOM, padx=5, pady=5, fill=tk.X)

    # Delete button
    delete_button = ttk.Button(right_frame, text="Delete", command=lambda: delete_student_data(student_treeview),
                               style='Btn.TButton')
    delete_button.pack(side=tk.BOTTOM, padx=5, pady=5, fill=tk.X)

    student_treeview = ttk.Treeview(right_frame, columns=student_labels, show="headings", height=1000)
    student_treeview.pack(fill=tk.BOTH, expand=True, padx=10, pady=100)

    for label in student_labels:
        student_treeview.heading(label, text=label, anchor=tk.CENTER)
        student_treeview.column(label, width=100)

    # Fetch data from the database and insert into the Treeview
    conn = db_connect()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student")
        rows = cursor.fetchall()
        for row in rows:
            student_treeview.insert("", "end", values=row)

    create_main_interface(parent_widget, action_frame, user)


def edit_student(student_treeview):
    selected_items = student_treeview.selection()
    if selected_items:
        # Get the selected student's data from the Treeview
        selected_student = student_treeview.item(selected_items[0])['values']
        # Open a new window or frame to display the selected student's details
        edit_window = tk.Toplevel(window)  # or tk.Tk() if you want a new window
        edit_window.title("Edit Student Details")

        window_width = 1000
        window_height = 600

        # Add labels and entry fields to display student details
        labels = ["ID", "Name", "Age", "Contact", "Address", "Enrollment Date", "Year", "Emergency Contact"]
        label_width = 150
        entry_width = 200
        row_height = 30
        label_entry_padx = 20
        label_entry_pady = 10
        start_y = (window_height - (len(labels) * row_height)) // 2  # Start Y position to center vertically

        entry_fields = {}  # Dictionary to hold entry fields

        for i, label_text in enumerate(labels):
            # Calculate X position to center horizontally
            label_x = (window_width - (2 * label_width + entry_width + 2 * label_entry_padx)) // 2
            entry_x = label_x + label_width + label_entry_padx

            # Calculate Y position
            y = start_y + i * row_height

            ttk.Label(edit_window, text=label_text).place(x=label_x, y=y, width=label_width, height=row_height)
            entry = ttk.Entry(edit_window)
            if i < len(selected_student):
                entry.insert(0, selected_student[i])  # Populate entry with student data
            entry.place(x=entry_x, y=y, width=entry_width, height=row_height)
            entry_fields[label_text] = entry  # Append entry field to entry_fields dictionary

        # Add button to update student details
        update_button = ttk.Button(edit_window, text="Update",
                                   command=lambda: update_student(edit_window, selected_student, entry_fields,
                                                                  student_treeview))
        update_button.place(x=(window_width - 100) // 2, y=start_y + len(labels) * row_height, width=100, height=30)


def update_student(edit_window, selected_student, entry_fields, student_treeview):
    # Get the updated data from entry fields
    updated_data = [entry_fields[label_text].get() for label_text in entry_fields.keys()]

    conn = db_connect()
    if conn:
        cursor = conn.cursor()
        try:
            # Construct the SQL query to update the student details
            query = """
            UPDATE stud_ms 
            SET Name = %s, Age = %s, Contact = %s, Address = %s, enroll_date = %s,
                Year = %s
            WHERE ID = %s
            """
            # Execute the query
            cursor.execute(query, (
                updated_data[1], updated_data[2], updated_data[3], updated_data[4],
                updated_data[5], updated_data[6], selected_student[0]  # Use student ID for WHERE clause
            ))
            # Commit changes to the database
            conn.commit()
            messagebox.showinfo("Success", "Student data saved successfully.")
            # Close the edit window
            edit_window.destroy()
            # Refresh the student listbox
            refresh_student_list(student_treeview)
        except pymysql.Error as e:
            messagebox.showinfo("Error", "Student data saved unsuccessfully.")
            # Rollback changes in case of error
            conn.rollback()
        finally:
            # Close cursor and connection
            cursor.close()
            conn.close()


def select_profile_pic(profile_pic_path):
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        profile_pic_path.set(file_path)


def upload_image_popup():
    student_id = simpledialog.askinteger("Upload Image", "Enter Student ID:")
    if student_id is not None:
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            update_profile_pic(student_id, file_path)


def update_profile_pic(student_id, file_path):
    conn = db_connect()
    if conn:
        cursor = conn.cursor()
        try:
            # Update the database with the new profile picture path for the student ID
            cursor.execute("UPDATE student SET profile_pic = %s WHERE ID = %s", (file_path, student_id))
            conn.commit()
            messagebox.showinfo("Success", "Student profile picture updated successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update student profile picture: {e}")
            conn.rollback()
        finally:
            conn.close()


def save_student_data(entry_fields, profile_pic_var, right_frame):
    id = entry_fields["id"].get()
    name = entry_fields["name"].get()
    age = entry_fields["age"].get()
    contact = entry_fields["contact"].get()
    address = entry_fields["address"].get()
    enroll_date = entry_fields["enrollment_date"].get()  # Use the correct key here
    year = entry_fields["year"].get()
    emergency_contact = entry_fields["emergency_contact"].get()

    Profile_pic = profile_pic_var.get()
    data = {label: entry_fields[label].get() for label in entry_fields}
    data["Profile Pic"] = Profile_pic

    conn = db_connect()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO student (ID, Name, Age, Contact, Address, enroll_date, Year, Emergency_Contact, Profile_Pic) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (
            id, name, age, contact, address, enroll_date, year, emergency_contact, Profile_pic))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student data saved successfully.")
        refresh_student_list(right_frame)
        for entry in entry_fields.values():
            entry.delete(0, tk.END)


def clear_fields(entry_fields):
    # Clear all entry fields
    for label in entry_fields:
        entry_fields[label].delete(0, tk.END)


def delete_student_data(student_listbox):
    # Placeholder for deleting student data from the database
    selected_item = student_listbox.selection()  # Use 'selection' instead of 'curselection'
    if selected_item:
        selected_id = student_listbox.item(selected_item, "values")[0]  # Extract the ID from the selected item

        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this student data?")
        if confirm:
            # Delete the selected data from the database
            conn = db_connect()
            if conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM student WHERE id = %s", (selected_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Student data deleted successfully.")
                # Refresh the student list after deletion
                refresh_student_list(student_listbox)
    else:
        messagebox.showwarning("No Selection", "Please select a student data to delete.")


def refresh_student_list(right_frame):
    # Clear existing data from the Treeview widget
    for child in right_frame.get_children():
        right_frame.delete(child)

    # Repopulate the Treeview widget with the latest data from the database
    conn = db_connect()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student")
        rows = cursor.fetchall()
        for row in rows:
            right_frame.insert('', 'end', values=row)
        conn.close()


# csv file
def upload_student_list(file_path, right_frame):
    # Connect to the database
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='tintots_kindergarden'
    )

    try:
        with connection.cursor() as cursor:
            # Open the CSV file for reading
            with open(file_path, 'r', newline='') as csvfile:
                csv_reader = csv.DictReader(csvfile)
                # Iterate over each row in the CSV file
                for row in csv_reader:
                    # Extract data from the CSV row
                    name = row['name']
                    age = int(row['age'])
                    contact = row['contact']
                    address = row['address']
                    # Convert date to 'YYYY-MM-DD' format
                    enroll_date = datetime.strptime(row['enroll_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
                    year = int(row['year'])
                    emergency_contact = row['emergency_contact']

                    # Insert the data into the database
                    sql = "INSERT INTO student (name, age, contact, address, enroll_date, year, emergency_contact) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql,
                                   (name, age, contact, address, enroll_date, year, emergency_contact))
            # Commit the transaction
            connection.commit()
            messagebox.showinfo("Success", "Student data saved successfully.")
            refresh_student_list(right_frame)
    except Exception as e:
        # Handle any errors
        print(f"Upload failed: {e}")
    finally:
        # Close the database connection
        connection.close()


def browse_file(student_treeview):
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        upload_student_list(file_path, student_treeview)


# class Slot
def show_class_slot(user, parent_widget, action_frame):
    # Clear existing widgets from the parent widget
    for widget in parent_widget.winfo_children():
        widget.destroy()

    # Create a new frame to display class slot details
    action_frame = tk.Frame(parent_widget)
    action_frame.pack(fill=tk.BOTH, expand=True)

    left_frame = tk.Frame(action_frame)
    left_frame.pack(side=tk.LEFT, padx=200, pady=350, fill=tk.BOTH, expand=True)

    # Subject details labels and entry fields
    ttk.Label(left_frame, text="Subject Code", style="CustomLabel.TLabel").grid(row=0, column=0, padx=10, pady=5,
                                                                                sticky="ns")
    subject_code_var = tk.StringVar()
    subject_code_combobox = ttk.Combobox(left_frame, textvariable=subject_code_var,
                                         values=["AT01", "AT02", "AT03", "BM01", "BM02", "BM03", "EG01", "EG02",
                                                 "EG03",
                                                 "LS01", "LS02", "LS03", "MS01", "MS02", "MS03", "MT01", "MT02",
                                                 "MT03",
                                                 "PE01", "PE02", "PE03", "SC01", "SC02", "SC03"])
    subject_code_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    # Subject Name
    ttk.Label(left_frame, text="Subject Name", style="CustomLabel.TLabel").grid(row=1, column=0, padx=10, pady=5,
                                                                                sticky="ns")
    subject_name_var = tk.StringVar()
    subject_name_combobox = ttk.Combobox(left_frame, textvariable=subject_name_var,
                                         values=["Art", "Bahasa Melayu", "English", "Living Skills", "Music",
                                                 "Mathematics", "Physical Education", "Science"])
    subject_name_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    # Year
    ttk.Label(left_frame, text="Year", style="CustomLabel.TLabel").grid(row=2, column=0, padx=10, pady=5,
                                                                        sticky="ns")
    year_var = tk.StringVar()
    year_combobox = ttk.Combobox(left_frame, textvariable=year_var, values=["1", "2", "3"])
    year_combobox.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    # Assigned
    ttk.Label(left_frame, text="Assigned", style="CustomLabel.TLabel").grid(row=3, column=0, padx=10, pady=5,
                                                                            sticky="ns")
    assigned_var = tk.StringVar()
    assigned_entry = ttk.Entry(left_frame, textvariable=assigned_var)
    assigned_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    # Day
    ttk.Label(left_frame, text="Day", style="CustomLabel.TLabel").grid(row=4, column=0, padx=10, pady=5,
                                                                       sticky="ns")
    day_var = tk.StringVar()
    day_combobox = ttk.Combobox(left_frame, textvariable=day_var,
                                values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    day_combobox.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    # Start Time
    ttk.Label(left_frame, text="Start Time", style="CustomLabel.TLabel").grid(row=5, column=0, padx=10, pady=5,
                                                                              sticky="ns")
    start_time_var = tk.StringVar()
    start_time_combobox = ttk.Combobox(left_frame, textvariable=start_time_var,
                                       values=["8:00", "10:00", "12:00", "15:00"])
    start_time_combobox.grid(row=5, column=1, padx=10, pady=5, sticky="w")

    # End Time
    ttk.Label(left_frame, text="End Time", style="CustomLabel.TLabel").grid(row=6, column=0, padx=10, pady=5,
                                                                            sticky="ns")
    end_time_var = tk.StringVar()
    end_time_combobox = ttk.Combobox(left_frame, textvariable=end_time_var,
                                     values=["10:00", "12:00", "14:00", "17:00"])
    end_time_combobox.grid(row=6, column=1, padx=10, pady=5, sticky="w")

    # Save button
    ttk.Button(left_frame, text="Save", command=lambda: save_class_slot(
        subject_code_var, subject_name_var, year_var, assigned_var, day_var, start_time_var, end_time_var,
        class_listbox
    ), style='Btn.TButton', width=35).grid(row=7, columnspan=6, padx=10, pady=10, )

    # Right frame for displaying class slot details
    right_frame = tk.Frame(action_frame, height=800, width=1000)
    right_frame.pack(side=tk.RIGHT, padx=100, pady=50, fill=tk.BOTH, expand=True)

    delete_button = ttk.Button(right_frame, text="Delete", command=lambda: delete_selected_data(class_listbox),
                               style='Btn.TButton')
    delete_button.pack(side=tk.BOTTOM, padx=5, pady=5, fill=tk.X)

    # Table to display class slot details
    columns = ("Subject Code", "Subject Name", "Year", "Assigned", "Day", "Start Time", "End Time")
    class_listbox = ttk.Treeview(right_frame, columns=columns, show="headings")
    class_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=110)

    # Set headings and column widths
    for col in columns:
        class_listbox.heading(col, text=col, anchor=tk.CENTER)
        class_listbox.column(col, width=100)  # Adjust column width as needed

    # Fetch data from the database and insert into the Treeview
    conn = db_connect()
    if conn:
        cursor = conn.cursor()
        try:
            # Perform a JOIN operation to combine data from both tables based on the code
            cursor.execute("""
                SELECT subject.code, subject.name, subject.year, subject.assigned, time_slot.day,
                       time_slot.start_time, time_slot.end_time
                FROM subject
                JOIN time_slot ON subject.code = time_slot.code  -- Corrected table name here
            """)
            rows = cursor.fetchall()
            for row in rows:
                class_listbox.insert("", "end", values=row)
        except Exception as e:
            print("Error executing SQL query:", e)
        finally:
            conn.close()

    create_main_interface(parent_widget, action_frame, user)

def save_class_slot(subject_code_var, subject_name_var, year_var, assigned_var, day_var, start_time_var,end_time_var,class_listbox):
    try:
        subject_code = subject_code_var.get()
        subject_name = subject_name_var.get()
        year = year_var.get()
        assigned = assigned_var.get()
        day = day_var.get()
        start_time = start_time_var.get()
        end_time = end_time_var.get()
        # Save subject details
        save_subject_details(subject_code, subject_name, year, assigned)
        # Save time slot details
        save_time_slot_details(subject_code, day, start_time, end_time)
        # Insert the new item into the Treeview
        class_listbox.insert("", "end",
                             values=(subject_code, subject_name, year, assigned, day, start_time, end_time))

        messagebox.showinfo("Success", "Class slot saved successfully.")
        subject_code_var.set('')
        subject_name_var.set('')
        year_var.set('')
        assigned_var.set('')
        day_var.set('')
        start_time_var.set('')
        end_time_var.set('')
        refresh_right_frame(class_listbox)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to save class slot: {e}")



def save_subject_details(code, subject_name, year, assigned):
    # Save subject details to subject table in the database
    conn = db_connect()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO subject (code, name, year, assigned) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (code, subject_name, year, assigned))
        conn.commit()
        conn.close()


def save_time_slot_details(code, day, start_time, end_time):
    # Save time slot details to time_slot table in the database
    conn = db_connect()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO time_slot (code, day, start_time, end_time) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (code, day, start_time, end_time))
        conn.commit()
        conn.close()


def delete_selected_data(class_listbox):
    # Get the selected item from the Treeview
    selected_item = class_listbox.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select an item to delete.")
        return
    # Get the values of the selected row
    values = class_listbox.item(selected_item, "values")
    subject_code = values[0]  # Assuming the subject code is the first column

    # Connect to the database
    conn = db_connect()
    if conn:
        try:
            cursor = conn.cursor()
            # Delete data from the 'time_slot' table first
            cursor.execute("DELETE FROM time_slot WHERE code = %s", (subject_code,))
            # Then delete data from the 'subject' table
            cursor.execute("DELETE FROM subject WHERE code = %s", (subject_code,))
            conn.commit()
            messagebox.showinfo("Success", "Data deleted successfully.")
            # Remove the selected item from the Treeview
            class_listbox.delete(selected_item)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete data: {e}")
        finally:
            conn.close()


def refresh_right_frame(class_listbox):
    # Clear existing items from the Treeview
    for item in class_listbox.get_children():
        class_listbox.delete(item)

    # Fetch updated data from the database and insert into the Treeview
    conn = db_connect()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT subject.code, subject.name, subject.year, subject.assigned, time_slot.day,
                       time_slot.start_time, time_slot.end_time
                FROM subject
                JOIN time_slot ON subject.code = time_slot.code
            """)
            rows = cursor.fetchall()
            for row in rows:
                class_listbox.insert("", "end", values=row)
        except Exception as e:
            print("Error executing SQL query:", e)
        finally:
            conn.close()


def logout(top_frame):
    top_frame.destroy()


window = tk.Tk()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(f"{screen_width}x{screen_height}")
action_frame = [tk.Frame(window)]
window.title("Tintots Kindergarden")
parent_widget = tk.Frame(window)

label_style = ttk.Style()
label_style.configure('Custom.TLabel', padding=(10, 5),
                      font=(font, 12),
                      foreground='black')

# Define the style for entry fields
entry_style = ttk.Style()
entry_style.configure('Custom.TEntry',
                      padding=(10, 5),
                      borderwidth=2,
                      relief='solid',
                      bordercolor='#000000',
                      borderradius=10)

# Define the style for buttons
button_style = ttk.Style()
button_style.configure('Custom.TButton', padding=5,
                       font=(font, 12),
                       foreground='#868686',
                       relief=tk.FLAT,
                       background='#F0E5F0',
                       borderwidth=50,
                       borderradius=30, )

# BUTTON STYLING #
backbtn_style = ttk.Style()
backbtn_style.configure('backBtn.TButton', padding=5,
                        font=(font, 12, 'bold'),
                        foreground='#7E467D',
                        relief=tk.FLAT,
                        borderwidth=0,
                        borderradius=20,
                        highlightthickness=0)

activebtn_style = ttk.Style()
activebtn_style.configure('activeBtn.TButton', padding=5,
                          font=(font, 13, 'bold'),
                          foreground='#7E467D',
                          relief=tk.FLAT,
                          borderwidth=50,
                          borderradius=30, )

aactivebtn_style = ttk.Style()
aactivebtn_style.configure('aactiveBtn.TButton', padding=8,
                           font=(font, 18, 'bold'),
                           foreground='#7E467D',
                           relief=tk.FLAT,
                           borderwidth=100,
                           borderradius=30, )

btn_style = ttk.Style()
btn_style.configure('Btn.TButton', padding=5,
                    font=(font, 13, 'bold'),
                    foreground='#7E467D',
                    relief=tk.FLAT,
                    borderwidth=30,
                    borderradius=30, )

sbtn_style = ttk.Style()
sbtn_style.configure('sBtn.TButton', padding=2,
                     font=(font, 12, 'bold'),
                     foreground='#7E467D',
                     relief=tk.FLAT,
                     borderwidth=25,
                     borderradius=30, )

inactivebtn_style = ttk.Style()
inactivebtn_style.configure('inactiveBtn.TButton', padding=5,
                            font=(font, 12),
                            foreground='#868686',
                            relief=tk.FLAT,
                            borderwidth=50,
                            borderradius=30, )

action_style = ttk.Style()
action_style.configure('actionBtn.TButton', padding=5,
                       font=(font, 12, 'bold'),
                       foreground='black',
                       relief=tk.FLAT,
                       borderwidth=50,
                       borderradius=30, )

action_style.configure('edit.TLabel', font=(font, 12, 'bold'), foreground='black', background='#F0E5F0')
action_style.configure('edit.TEntry', font=(font, 12), padding=(5, 5, 5, 5))
action_style.configure('edit.TLabelframe', font=(font, 20, "bold"), bd=3, padding=(20, 20), background='#F0E5F0')
action_style.configure('general.TLabelframe', font=(font, 20, "bold"), bd=3, padding=(20, 20), background='white')
style = ttk.Style()
style.configure("CustomLabel.TLabel", font=("Lato", 12))
custom_font = ("Lato", 28)
label_font = ('Arial', 14)

Frame_buttonNav = tk.Frame(window, bd=5, relief=tk.FLAT, bg="#F0E5F0")

label = tk.Label(window, text="Tintots Kindergarden", font=custom_font)
label.pack(pady=50)
# Main buttons frame
main_buttons_frame = tk.Frame(window)
main_buttons_frame.pack(pady=150)

# Admin button
admin_button = ttk.Button(main_buttons_frame, text="Admin", command=open_admin_login, style="aactiveBtn.TButton",
                          width=100)
admin_button.grid(row=0, column=0, padx=50)

# Staff button
staff_button = ttk.Button(main_buttons_frame, text="Staff", command=staff_login, style="aactiveBtn.TButton",
                          width=100)
staff_button.grid(row=1, column=0, padx=50)

# Admin login frame
admin_login_frame = tk.Frame(window)

# Create username and password labels and entry widgets
admin_username_label = ttk.Label(admin_login_frame, text="Username:", style="CustomLabel.TLabel")
admin_username_label.pack()

admin_username_entry = ttk.Entry(admin_login_frame)
admin_username_entry.pack()

admin_password_label = ttk.Label(admin_login_frame, text="Password:", style="CustomLabel.TLabel")
admin_password_label.pack()

admin_password_entry = ttk.Entry(admin_login_frame, show="*")
admin_password_entry.pack()

# Create the login button and pass admin_username_entry and admin_password_entry to admin_authenticate
admin_login_button = ttk.Button(admin_login_frame, text="Admin Login",
                                command=lambda: admin_authenticate(admin_username_entry, admin_password_entry),
                                style="aactiveBtn.TButton", width=50)
admin_login_button.pack(pady=10)

# Staff login frame
staff_login_frame = tk.Frame(window)

staff_username_label = ttk.Label(staff_login_frame, text="Username:", style="CustomLabel.TLabel")
staff_username_label.pack()

staff_username_entry = ttk.Entry(staff_login_frame, width=40, font=label_font)
staff_username_entry.pack()

staff_password_label = ttk.Label(staff_login_frame, text="Password:", style="CustomLabel.TLabel")
staff_password_label.pack()

staff_password_entry = ttk.Entry(staff_login_frame, show="*", width=40, font=label_font)
staff_password_entry.pack()

staff_login_button = ttk.Button(staff_login_frame, text="Login", command=staff_authenticate,
                                style="aactiveBtn.TButton", width=50)
staff_login_button.pack(pady=10)

window.mainloop()




