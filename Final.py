from tkinter import ttk, simpledialog
from tkinter import messagebox
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
import csv
import pymysql
from datetime import datetime
from tkcalendar import DateEntry

font = 'Lato'
years = [1, 2, 3]
year1_subject=['Bahasa Melayu','English']
year2_subject=['Art','Science','Mathematics']
year3_subject=['Living Skills','Music','Physical Education']

### General Functions ####
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

def display_userPic(frame, width, height, user, table):
    connection = pymysql.connect(host='localhost', user='root', password='', database='tintots_kindergarden')
    try:
        with connection.cursor() as cursor:
            sql = f"SELECT profile_pic FROM {table} WHERE id=%s;"
            cursor.execute(sql, (user,))
            # Fetch the result
            result = cursor.fetchone()
            if result:
                image_path = result[-1]  # Assuming the profile_pic column is the first column in the result
            else:
                # Handle case where no result is found
                image_path = None
    finally:
        # Close the connection
        connection.close()

    if image_path:
        load_profilePic(frame, width, height, image_path)


def load_profilePic(frame, width, height, image_path):
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
    label.grid(row=0, column=0, padx=15, pady=15)


def fetch_user(user, table):
    connection = pymysql.connect(host='localhost', user='root', password='', database='tintots_kindergarden')
    try:
        sql = f"SELECT * FROM {table} WHERE id=%s;"
        with connection.cursor() as cursor:
            cursor.execute(sql, (user,))
            result = cursor.fetchone()
            if result:
                if table == 'staff':
                    user_info['id'] = result[0]
                    user_info['name'] = result[1]
                    user_info['contact'] = result[2]
                    user_info['password'] = result[3]
                    user_info['age'] = result[4]
                    user_info['address'] = result[5]
                    user_info['email'] = result[6]
                    user_info['qualification'] = result[7]
                    user_info['position'] = result[8]
                    user_info['department'] = result[9]
                    user_info['salary'] = result[10]
                    user_info['profile_pic'] = result[11]
                    return user_info
                elif table == 'student':
                    stud_info['id'] = result[0]
                    stud_info['name'] = result[1]
                    stud_info['age'] = result[2]
                    stud_info['contact'] = result[3]
                    stud_info['address'] = result[4]
                    stud_info['enroll_date'] = result[5]
                    stud_info['year'] = result[6]
                    stud_info['annual_review'] = result[7]
                    stud_info['profile_pic'] = result[8]
                    return stud_info
            else:
                tk.messagebox.showerror("Error", "User not found.")
                return

    except Exception as e:
        tk.messagebox.showerror("Error", f"Database error: {str(e)}")
        return

def edit_profile():
    # Create a pop-up window for editing
    edit_window = tk.Toplevel(window, bg='#F0E5F0')
    edit_window.title("Edit Profile")
    edit_window.geometry(f"+300+150")
    edit_detail = ttk.LabelFrame(edit_window, style='edit.TLabelframe')
    edit_detail.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Entry widgets to display and edit user info
    entries = {}
    editrow = 0
    for field, value in user_info.items():
        if field in ["id", "name", "password", "email", "contact", "address"]:
            ttk.Label(edit_detail, text=field.capitalize() + ":", style='edit.TLabel').grid(row=editrow, column=0,
                                                                                            padx=5,
                                                                                            pady=10, sticky="w")
            entry = ttk.Entry(edit_detail, style='edit.TEntry')
            entry.insert(0, value)
            entry.grid(row=editrow, column=1, padx=10, pady=10, sticky="w")
            entries[field] = entry
            if field == "id":
                entry.config(state="readonly")

            editrow += 1

    # Function to save the changes made by the user
    def save_changes(user_info):
        connection = pymysql.connect(host='localhost', user='root', password='', database='tintots_kindergarden')

        new_name = entries['name'].get()
        new_password = entries['password'].get()
        new_email = entries['email'].get()
        new_contact = entries['contact'].get()
        new_address = entries['address'].get()
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE staff SET name=%s, contact=%s, password=%s,  address=%s, email=%s WHERE id=%s;"
                print(sql, (new_name, new_contact, new_password, new_address, new_email, user_info['id']))
                cursor.execute(sql, (new_name, new_contact, new_password, new_address, new_email, user_info['id']))
                connection.commit()
                edit_window.destroy()
                tk.messagebox.showinfo("Success", "Profile updated successfully")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Database error: {str(e)}")
            edit_window.destroy()

    # Button to save changes
    save_button = ttk.Button(edit_detail, text="Save Changes", command=lambda: save_changes(user_info),
                             style='actionBtn.TButton')
    save_button.grid(row=editrow, column=0, columnspan=2, padx=5, pady=10)

def display_user_data(frame):
    global profile_ctrlRow
    for field, value in user_info.items():
        value = str(value)
        if field == 'profile_pic' or field == 'password' or field == 'salary' or field == 'qualification':
            pass
        else:
            if profile_ctrlRow <= 5 or (user_info['department'] == 'Administration'):
                ttk.Label(frame, text=field.capitalize() + ":", style='edit.TLabel',
                          background='white').grid(row=profile_ctrlRow, column=0,
                                                   padx=10,
                                                   pady=5, sticky="w")
                ttk.Label(frame, text=value, style='edit.TLabel', font=('normal',12), background='white',
                          width=15).grid(row=profile_ctrlRow, column=1, padx=10,
                                         pady=5, sticky="w")
            else:
                ttk.Label(frame, text=field.capitalize() + ":", style='edit.TLabel',
                          background='white').grid(row=profile_ctrlRow - 6, column=3,
                                                   padx=10,
                                                   pady=5, sticky="w")
                ttk.Label(frame, text=value, style='edit.TLabel', font=('normal',12), background='white').grid(
                    row=profile_ctrlRow - 6, column=4, padx=10,
                    pady=5, sticky="w")
        profile_ctrlRow+=1

def logout():
    for widget in window.winfo_children():
        widget.destroy()
    login()

def greeting():
    # Get the current time
    current_time = datetime.now().time()
    # Extract the hour from the current time
    hour = current_time.hour
    # Determine the greeting based on the hour
    if 6 <= hour < 12:
        return "Good Morning"
    elif 12 <= hour < 18:
        return "Good Afternoon"
    else:
        return "Good Evening"

def select_profile_pic(profile_pic_path):
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        profile_pic_path.set(file_path)

####### General functions ends here #########

def admin_authenticate(loginframe,admin_username_entry, admin_password_entry):
    # Get username and password
    username = admin_username_entry.get()
    password = admin_password_entry.get()

    # Check if ID is an 8-digit integer
    if len(username) != 8 or not username.isdigit():
        messagebox.showerror("Admin Login", "Invalid username format. Please enter an 8-digit ID number.")
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
                loginframe.destroy()
                admin_main_interface(result)  # Pass the parent widget, user details, and action frame
            else:
                messagebox.showerror("Admin Login", "Invalid username or password.")
        except pymysql.Error as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")
        finally:
            conn.close()
    else:
        messagebox.showerror("Error", "Failed to connect to database.")

def admin_main_interface(user):
    global user_info
    # Clear existing widgets from the parent frame
    for widget in window.winfo_children():
        widget.destroy()

    user_id = user[0]
    user_info = fetch_user(user_id, 'staff')

    # Create a new frame to display user details
    Frame_adminProfile = tk.Frame(window, bd=5, bg="white")
    Frame_adminProfile.place(x=0,y=0,width=int(window.winfo_width()*0.35),height=window.winfo_height())
    display_userPic(Frame_adminProfile, 180, 180, user_id,'staff')

    display_user_data(Frame_adminProfile)

    logout_button = ttk.Button(Frame_adminProfile, text="Log Out", command=lambda: logout(),
                               style='actionBtn.TButton', width=15)
    logout_button.grid(row=profile_ctrlRow+2, rowspan=2,column=0, padx=5, pady=35)

    Editprofile_button = ttk.Button(Frame_adminProfile, text="Edit Profile", command=lambda: edit_profile(),
                                    style='actionBtn.TButton', width=15)
    Editprofile_button.grid(row=profile_ctrlRow+2,rowspan=2, column=1, padx=5, pady=35)

    greet=greeting()
    Frame_adminBoard = tk.Frame(window, bd=5,background='#F0E5F0',pady=50,padx=50)
    Frame_adminBoard.place(x=int(window.winfo_width()*0.35),y=0,width=int(window.winfo_width()*0.65),height=window.winfo_height())
    head_lbl=ttk.Label(Frame_adminBoard,style='edit.TLabel',font=(font,18),text=greet+' Admin \n\nWhat\'s on the agenda for today?')
    head_lbl.grid(row=0,column=0,columnspan=3)

    staffData_button = ttk.Button(Frame_adminBoard, text="Staff Data", command=lambda: edit_profile(),
                                    style='activeBtn.TButton', width=15)
    staffData_button.grid(row=1, column=0,columnspan=2, padx=5, pady=25,sticky='we')
    studentData_button = ttk.Button(Frame_adminBoard, text="Student Data", command=lambda: show_student_data(user),
                                  style='activeBtn.TButton', width=15)
    studentData_button.grid(row=2, column=0, columnspan=2, padx=5, pady=25, sticky='we')
    classSlot_button = ttk.Button(Frame_adminBoard, text="Class Slot", command=lambda: show_class_slot(user),
                                  style='activeBtn.TButton', width=15)
    classSlot_button.grid(row=3, column=0, columnspan=2, padx=5, pady=25, sticky='we')

def refresh_treetable(treetable):
    # Clear existing data from the Treeview widget
    treetable.delete(*treetable.get_children())

    # Repopulate the Treeview widget with the latest data from the database
    list=fetch_all_stud()
    for row in list:
        treetable.insert('', 'end', values=row)

### Class Slot ###
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
            cursor.execute("DELETE FROM time_slot WHERE subject = %s", (subject_code,))
            # Then delete data from the 'subject' table
            cursor.execute("DELETE FROM subject WHERE code = %s", (subject_code,))
            conn.commit()
            messagebox.showinfo("Success", "Subject deleted successfully.")
            # Remove the selected item from the Treeview
            class_listbox.delete(selected_item)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete data: {e}")
        finally:
            conn.close()


def save_class_slot(subject_code_var, subject_name_var, year_var, assigned_var, day_var, start_time_var,end_time_var,class_listbox):
    try:
        subject_code = subject_code_var.get()
        subject_name = subject_name_var.get()
        year = year_var.get()
        assigned = assigned_var.get()
        day = day_var.get()
        start_time = start_time_var.get()
        end_time = end_time_var.get()
        if check_subject_exists(subject_code):
            # Save time slot details
            save_time_slot_details(subject_code, day, start_time, end_time)
        else:
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
        subject_load_data(class_listbox)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to save class slot: {e}")

def check_subject_exists(subject_code):
    # Check if the subject code exists in the subject table
    conn = db_connect()
    if conn:
        cursor = conn.cursor()
        query = "SELECT code FROM subject WHERE code = %s"
        cursor.execute(query, (subject_code,))
        result = cursor.fetchone()
        if result:
            return result is not None
        conn.close()
    return False

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
        query = "INSERT INTO time_slot (subject, day, start_time, end_time) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (code, day, start_time, end_time))
        conn.commit()
        conn.close()

def show_class_slot(user):
    # Clear existing widgets
    for widget in window.winfo_children():
        widget.destroy()

    back_button = ttk.Button(window, style='activeBtn.TButton', text='Back', command=lambda: admin_main_interface(user))
    back_button.place(x=10, y=10)

    # Left frame for data entry
    left_frame = tk.Frame(window, bg='white',pady=10,padx=10)
    left_frame.place(x=0, y=50, width=int(window.winfo_width() * 0.30), height=int(window.winfo_height() - 30))

    right_frame = tk.Frame(window, bg='#F0E5F0')
    right_frame.place(x=int(window.winfo_width() * 0.25), y=0, width=int(window.winfo_width() * 0.75),
                      height=int(window.winfo_height()))
    right_frame.columnconfigure(0, weight=1)
    right_frame.columnconfigure(1, weight=1)
    right_frame.grid_rowconfigure(1, weight=1)

    # Subject details labels and entry fields
    ttk.Label(left_frame, text="Subject Code", style="general.TLabel").grid(row=0, column=0, padx=10, pady=5,
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
    ttk.Label(left_frame, text="Subject Name", style="general.TLabel").grid(row=1, column=0, padx=10, pady=5,
                                                                                sticky="ns")
    subject_name_var = tk.StringVar()
    subject_name_combobox = ttk.Combobox(left_frame, textvariable=subject_name_var,
                                         values=["Art", "Bahasa Melayu", "English", "Living Skills", "Music",
                                                 "Mathematics", "Physical Education", "Science"])
    subject_name_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    # Year
    ttk.Label(left_frame, text="Year", style="general.TLabel").grid(row=2, column=0, padx=10, pady=5,
                                                                        sticky="ns")
    year_var = tk.StringVar()
    year_combobox = ttk.Combobox(left_frame, textvariable=year_var, values=["1", "2", "3"])
    year_combobox.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    #Assigned
    ttk.Label(left_frame, text="Assigned", style="general.TLabel").grid(row=3, column=0, padx=10, pady=5,
                                                                        sticky="ns")
    academic_staff = []  # Initialize an empty list to store academic staff names
    conn = db_connect()
    if conn:  # Assuming you have a database connection object named 'conn'
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT name FROM staff WHERE department = 'Academic'")
            academic_staff = [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print("Error fetching academic staff:", e)
        finally:
            conn.close()

    # Create a dropdown menu with academic staff names
    assigned_var = tk.StringVar()
    assigned_var.set('Teacher')
    assigned_dropdown = ttk.Combobox(left_frame, textvariable=assigned_var, values=academic_staff, state="readonly")
    assigned_dropdown.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    # Day
    ttk.Label(left_frame, text="Day", style="general.TLabel").grid(row=4, column=0, padx=10, pady=5,
                                                                       sticky="ns")
    day_var = tk.StringVar()
    day_combobox = ttk.Combobox(left_frame, textvariable=day_var,
                                values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    day_combobox.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    # Start Time
    ttk.Label(left_frame, text="Start Time", style="general.TLabel").grid(row=5, column=0, padx=10, pady=5,
                                                                              sticky="ns")
    start_time_var = tk.StringVar()
    start_time_combobox = ttk.Combobox(left_frame, textvariable=start_time_var,
                                       values=["8:00", "10:00", "12:00", "15:00"])
    start_time_combobox.grid(row=5, column=1, padx=10, pady=5, sticky="w")

    # End Time
    ttk.Label(left_frame, text="End Time", style="general.TLabel").grid(row=6, column=0, padx=10, pady=5,
                                                                            sticky="ns")
    end_time_var = tk.StringVar()
    end_time_combobox = ttk.Combobox(left_frame, textvariable=end_time_var,
                                     values=["10:00", "12:00", "14:00", "17:00"])
    end_time_combobox.grid(row=6, column=1, padx=10, pady=5, sticky="w")

    # Save button
    ttk.Button(left_frame, text="Save", command=lambda: save_class_slot(
        subject_code_var, subject_name_var, year_var, assigned_var, day_var, start_time_var, end_time_var,
        class_listbox
    ), style='activeBtn.TButton').grid(row=7, columnspan=2, padx=10, pady=10,sticky='we')


    delete_button = ttk.Button(left_frame, text="Delete", command=lambda: delete_selected_data(class_listbox),
                               style='activeBtn.TButton')
    delete_button.grid(row=8, columnspan=2, padx=10, pady=10,sticky='we')

    # Table to display class slot details
    timetable_lbl=ttk.Label(right_frame,text='Time Table',style='heading.TLabel').grid(row=0,padx=10,pady=20)
    columns = ("Subject Code", "Subject Name", "Year", "Assigned", "Day", "Start Time", "End Time")
    class_listbox = ttk.Treeview(right_frame, columns=columns, show="headings",style="general.Treeview")
    class_listbox.grid(row=1,padx=10, pady=10, sticky='nsew')

    # Set headings and column widths
    for col in columns:
        class_listbox.heading(col, text=col, anchor=tk.CENTER)
        class_listbox.column(col,width=int(window.winfo_width() * 0.75 / 7))  # Adjust column width as needed
    subject_load_data(class_listbox)

def subject_load_data(treeview):
    # Fetch data from the database and insert into the Treeview
    treeview.delete(*treeview.get_children())
    conn = db_connect()
    if conn:
        cursor = conn.cursor()
        try:
            # Perform a JOIN operation to combine data from both tables based on the code
            cursor.execute("""
                SELECT subject.code, subject.name, subject.year, subject.assigned, time_slot.day,time_slot.start_time, time_slot.end_time
                FROM subject
                LEFT JOIN time_slot ON subject.code = time_slot.subject;
            """)
            rows = cursor.fetchall()
            for row in rows:
                treeview.insert("", "end", values=row)
        except Exception as e:
            print("Error executing SQL query:", e)
        finally:
            conn.close()
### Class Slot ends here ###


### Show Student Data ###

def fetch_all_stud():
    connection = pymysql.connect(host='localhost',user='root',password='',database='tintots_kindergarden')
    cursor = connection.cursor()
    try:
        sql = "SELECT * FROM student ;"
        cursor.execute(sql)
        all_stud = cursor.fetchall()
        print(all_stud)
        if all_stud:
            for row in all_stud:
                all_student_IdName[row[0]] = row[1]
        else:
            tk.messagebox.showerror("Error", "No Student Found!")
        return all_stud  # Return the value of all_stud
    except Exception as e:
        tk.messagebox.showerror("Error", f"Database error: {str(e)}")

def search_students(treetable,list):
    search_text = search_entry.get()

    if not search_text:
        # If search text is empty, reset the tree to show all items
        refresh_treetable(treetable)
        return
    else:
        searching.clear()
        for stud in list:
            if search_text.isdigit():
                if int(search_text) == stud[0]:
                    searching.append(stud)
            else:
                if search_text.lower() in stud[1].lower():
                    searching.append(stud)

        if searching:
            treetable.delete(*treetable.get_children())
            for row in searching:
                treetable.insert('', 'end', values=row)

        else:
            tk.messagebox.showinfo("No Student Found", "No student matching the search criteria was found.")

def save_student_data(entry_fields, profile_pic_var, treetable):
    # Extract student data from entry fields
    name = entry_fields["name"].get()
    age = entry_fields["age"].get()
    contact = entry_fields["contact"].get()
    address = entry_fields["address"].get()
    enroll_date = entry_fields["enrollment_date"].get()
    year = entry_fields["year"].get()

    Profile_pic = profile_pic_var.get()
    data = {label: entry_fields[label].get() for label in entry_fields}
    data["Profile Pic"] = Profile_pic

    conn = db_connect()
    if conn:
        cursor = conn.cursor()

        try:
            # Insert student data into the student table
            student_query = "INSERT INTO student (name, age, contact, address, enroll_date, year, profile_pic) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(student_query, (name, age, contact, address, enroll_date, year, Profile_pic))
            conn.commit()

            # Get the auto-generated student ID
            stud_id = cursor.lastrowid

            # Insert subject records into the marks_record table based on the student's academic year
            subject_query = "INSERT INTO marks_record (subject, stud_id, stud_name) VALUES (%s, %s, %s)"
            subjects = []

            if year == "1":
                subjects = year1_subject
            elif year == "2":
                subjects = year2_subject
            elif year == "3":
                subjects = year3_subject

            for subject in subjects:
                cursor.execute(subject_query, (subject, stud_id, name))
                conn.commit()

            messagebox.showinfo("Success", "Student data saved successfully.")
            refresh_treetable(treetable)

            for entry in entry_fields.values():
                entry.delete(0, tk.END)

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Failed to save student data: {str(e)}")

        conn.close()

def clear_fields(entry_fields, add_button, edit_button, delete_button, clear_btn):
    # Clear all entry fields
    for label in entry_fields:
        entry_fields[label].delete(0, tk.END)
    add_button['state'] = 'enabled'
    edit_button['state'] = 'disabled'
    delete_button['state'] = 'disabled'
    clear_btn['state'] = 'enabled'

#upload csv file
def browse_file(student_treeview):
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        upload_student_list(file_path, student_treeview)

# csv file
def upload_student_list(file_path, treetable):
    # Connect to the database
    connection = pymysql.connect(host='localhost',user='root',password='',database='tintots_kindergarden')

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
                    sql = "INSERT INTO student (name, age, contact, address, enroll_date, year, emergency_contact) VALUES (%s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql,
                                   (name, age, contact, address, enroll_date, year))
            # Commit the transaction
            connection.commit()
            messagebox.showinfo("Success", "Student data saved successfully.")
            refresh_treetable(treetable)
    except Exception as e:
        # Handle any errors
        print(f"Upload failed: {e}")
    finally:
        # Close the database connection
        connection.close()

def delete_student_data(student_listbox,list):
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
                refresh_treetable(student_listbox)
    else:
        messagebox.showwarning("No Selection", "Please select a student data to delete.")

def propagate_selected_row(event, treeview, labels, entry_fields, add_button, edit_button, delete_button, clear_btn):
    # Get the selected item
    selected_item = treeview.selection()
    if selected_item:
        # Get the values of the selected row
        values = treeview.item(selected_item, "values")
        # Update the entry fields with the selected row's values
        for label, value in zip(labels, values):

            entry_field = entry_fields[label.lower().replace(" ", "_")]
            entry_field.delete(0, tk.END)
            entry_field.insert(0, value)
            if label == 'ID':
                entry_field.config(state='disabled')

        # Disable the ADD and CLEAR buttons, and enable the EDIT and DELETE buttons
        add_button['state'] = 'disabled'
        edit_button['state'] = 'enabled'
        delete_button['state'] = 'enabled'
        clear_btn['state'] = 'enabled'
        # Disable the ID entry field

def update_student(entry_fields, student_treeview):
    # Get the updated data from entry fields
    id = entry_fields["id"].get()
    name = entry_fields["name"].get()
    age = entry_fields["age"].get()
    contact = entry_fields["contact"].get()
    address = entry_fields["address"].get()
    enroll_date = entry_fields["enrollment_date"].get()
    year = entry_fields["year"].get()

    conn = db_connect()
    if conn:
        cursor = conn.cursor()
        try:
            # Construct the SQL query to update the student details
            query = """
            UPDATE student
            SET name = %s, age = %s, contact = %s, address = %s, enroll_date = %s,
                year = %s
            WHERE id = %s
            """
            # Execute the query
            cursor.execute(query, (name, age, contact, address, enroll_date, year, id))
            # Commit changes to the database
            conn.commit()
            messagebox.showinfo("Success", "Student data saved successfully.")

            # Refresh the student listbox
            refresh_treetable(student_treeview)
        except pymysql.Error as e:
            messagebox.showinfo("Error", "Student data saved unsuccessfully.")
            # Rollback changes in case of error
            conn.rollback()
        finally:
            # Close cursor and connection
            cursor.close()
            conn.close()

def show_student_data(user):
    # Clear existing widgets from the parent frame
    for widget in window.winfo_children():
        widget.destroy()

    all_stud = fetch_all_stud()

    back_button=ttk.Button(window,style='activeBtn.TButton',text='Back',command=lambda: admin_main_interface(user))
    back_button.place(x=10,y=10)

    # Left frame for data entry
    left_frame = tk.Frame(window,bg='white')
    left_frame.place(x=0, y=50, width=int(window.winfo_width() * 0.30), height=int(window.winfo_height()-30))

    right_frame = tk.Frame(window, bg='#F0E5F0')
    right_frame.place(x=int(window.winfo_width() * 0.25), y=0, width=int(window.winfo_width() * 0.75), height=int(window.winfo_height()))
    right_frame.columnconfigure(0, weight=1)
    right_frame.columnconfigure(1, weight=1)
    right_frame.grid_rowconfigure(1, weight=1)

    global search_entry

    search_entry = ttk.Entry(right_frame, width=30, style='edit.TEntry')
    search_entry.grid(row=0, column=0, padx=10, pady=10, sticky='e')
    # Create the search button
    search_button = ttk.Button(right_frame, text="Search", style='actionBtn.TButton',command=lambda: search_students(student_treeview,all_stud) )
    search_button.grid(row=0, column=1, padx=10, pady=10, sticky='w')

    # Entry fields labels
    student_labels = ["ID", "Name", "Age", "Contact", "Address", "Enrollment Date", "Year"]

    # Entry fields
    entry_fields = {}
    for i, label in enumerate(student_labels, start=1):
        entry_lbl=ttk.Label(left_frame, text=label, style='general.TLabel')
        entry_lbl.grid(row=i, column=0, padx=10, pady=10)

        # Create entry field widgets for all labels except 'Year' and 'Enrollment Date'
        if label != "Year" and label != "Enrollment Date":
            entry_fields[label.lower().replace(" ", "_")] = ttk.Entry(left_frame,style='edit.TEntry')
            entry_fields[label.lower().replace(" ", "_")].grid(row=i, column=1, padx=10, pady=5)
        elif label == "Year":
            # Create a dropdown menu for the 'Year' field
            year_combobox = ttk.Combobox(left_frame, values=years, state="readonly")
            year_combobox.grid(row=i, column=1, padx=10, pady=5)
            entry_fields[label.lower().replace(" ", "_")] = year_combobox
        else:  # label == "Enrollment Date"
            # Create a DateEntry widget for selecting the date
            enrollment_date_entry = DateEntry(left_frame, date_pattern="yyyy-mm-dd")
            enrollment_date_entry.grid(row=i, column=1, padx=10, pady=5)
            entry_fields[label.lower().replace(" ", "_")] = enrollment_date_entry

    # Profile pic selection button
    profile_pic_var = tk.StringVar()
    profile_pic_label = ttk.Label(left_frame, text="Profile Picture", style='general.TLabel')
    profile_pic_label.grid(row=len(student_labels)+1, column=0, padx=10, pady=5)
    profile_pic_button = ttk.Button(left_frame, text="Select Profile Picture",
                                    command=lambda: select_profile_pic(profile_pic_var), style='Btn.TButton')
    profile_pic_button.grid(row=len(student_labels)+1, column=1, padx=10, pady=5)

    add_button = ttk.Button(left_frame, text="ADD",
                             command=lambda: save_student_data(entry_fields, profile_pic_var, student_treeview),
                             style='activeBtn.TButton')
    add_button.grid(row=len(student_labels) + 2, column=0,padx=2, pady=2, sticky="we")

    # Clear fields button
    clear_btn=ttk.Button(left_frame, text="CLEAR", command=lambda: clear_fields(entry_fields, add_button, edit_button, delete_button, clear_btn),
               style='activeBtn.TButton')
    clear_btn.grid(row=len(student_labels) + 3, column=0, padx=2, pady=2, sticky="we")

    upload_button = ttk.Button(left_frame, text="Upload Student List", command=lambda: browse_file(student_treeview),
                               style='actionBtn.TButton')
    upload_button.grid(row=len(student_labels) + 4, columnspan=2, padx=2, pady=20, sticky="we")

    # update_image_button = ttk.Button(right_frame, text="Update Image", command=upload_image_popup,
    #                                  style='Btn.TButton')
    # update_image_button.pack(side=tk.BOTTOM, padx=5, pady=5, fill=tk.X)

    edit_button = ttk.Button(left_frame, text="UPDATE", command=lambda: update_student(entry_fields,student_treeview),
                             style='activeBtn.TButton')
    edit_button.grid(row=len(student_labels) + 3, column=1, padx=2, pady=2, sticky="we")

    # Delete button
    delete_button = ttk.Button(left_frame, text="DELETE", command=lambda: delete_student_data(student_treeview,all_stud),
                               style='activeBtn.TButton')
    delete_button.grid(row=len(student_labels) + 2,column=1, padx=2, pady=2, sticky="we")

    add_button['state'] = 'enabled'
    edit_button['state'] = 'disabled'
    delete_button['state'] = 'disabled'
    clear_btn['state'] = 'enabled'

    #Student Table
    student_treeview = ttk.Treeview(right_frame, columns=student_labels, show="headings",style="general.Treeview")
    student_treeview.grid(row=1, columnspan=2,padx=10, pady=10, sticky='nsew')
    for label in student_labels:
        student_treeview.heading(label, text=label, anchor=tk.CENTER)
        student_treeview.column(label, width=100)
    for row in all_stud:
        student_treeview.insert("", "end", values=row)
    student_treeview.bind("<<TreeviewSelect>>", lambda event: propagate_selected_row(event,student_treeview,student_labels,entry_fields, add_button, edit_button, delete_button, clear_btn))

### Student Data ends here ####


window = tk.Tk()
screen_width = window.winfo_screenwidth() * 0.99
screen_height = window.winfo_screenheight()* 0.99
window.geometry(f"{int(screen_width)}x{int(screen_height)}+0+0")
window.title("Tintots Kindergarden")
window.configure(bg="#f0e5f0")

def login():
    global user_info, stud_info, all_student_IdName, all_stud, profile_ctrlRow, searching,add_button,edit_button,delete_button,clear_btn
    user_info = {}
    stud_info = {}
    all_student_IdName = {}
    all_stud=()
    profile_ctrlRow = 1
    searching=[]
    add_button= None
    edit_button=None
    delete_button=None
    clear_btn=None
    login_frame = tk.Frame(window, background="white",padx=30,pady=30)
    login_frame.pack(expand=True)
    login_frame.columnconfigure(1, weight=1)

    title_lbl = ttk.Label(login_frame, text="Tintots Kindergarden", font=(font,20),style='heading.TLabel')
    title_lbl.grid(row=0, columnspan=2, padx=50, pady=50)

    # Create username and password labels and entry widgets
    username_label = ttk.Label(login_frame, text="User ID:", style="general.TLabel")
    username_label.grid(row=1, column=0, padx=10, pady=10)
    username_entry = ttk.Entry(login_frame, width=40, style="edit.TEntry")
    username_entry.grid(row=1, column=1, padx=10, pady=10)

    password_label = ttk.Label(login_frame, text="Password:", style="general.TLabel")
    password_label.grid(row=2, column=0, padx=10, pady=10)
    password_entry = ttk.Entry(login_frame, show="*", width=40, style='edit.TEntry')
    password_entry.grid(row=2, column=1, padx=10, pady=10)

    # Admin login button
    admin_button = ttk.Button(login_frame, text="Admin Login", style="activeBtn.TButton", command=lambda: admin_authenticate(login_frame,username_entry, password_entry))
    admin_button.grid(row=3, columnspan=2)

    # Teacher login button
    staff_button = ttk.Button(login_frame, text="Teacher Login",  style="activeBtn.TButton")
    staff_button.grid(row=4, columnspan=2)

    # Forgot pswd button
    fpswd_button = ttk.Button(login_frame, text="Forgot Password",  style="actionBtn.TButton")
    fpswd_button.grid(row=5, columnspan=2,pady=20,sticky='ew')

if __name__ == "__main__":
    login()

## General Setting ##
btn_style = ttk.Style()
btn_style.configure('activeBtn.TButton', padding=5,
                          font=(font, 13, 'bold'),
                          foreground='#7E467D',
                          relief=tk.FLAT,
                          borderwidth=50,
                          borderradius=30, )

btn_style.configure('inactiveBtn.TButton', padding=5,
                            font=(font, 12),
                            foreground='#868686',
                            relief=tk.FLAT,
                            borderwidth=50,
                            borderradius=30, )


btn_style.configure('actionBtn.TButton', padding=5,
                       font=(font, 12, 'bold'),
                       foreground='black',
                       relief=tk.FLAT,
                       borderwidth=50,
                       borderradius=30, ) ## for login, back

action_style = ttk.Style()
action_style.configure('edit.TLabel', font=(font, 12, 'bold'), foreground='black', background='#F0E5F0')  #for edit profile label
action_style.configure('heading.TLabel', font=(font, 15, 'bold'), foreground='#7E467D', background='white') #for heading label
action_style.configure('general.TLabel', font=(font, 12), foreground='black', background='white') #for general label

action_style.configure('edit.TEntry', font=(font, 14), padding=(5, 5, 5, 5))

action_style.configure('edit.TLabelframe', font=(font, 20, "bold"), bd=3, padding=(20, 20), background='#F0E5F0',
                       foreground='black')
action_style.configure('general.TLabelframe', font=(font, 20, "bold"), bd=3, padding=(20, 20), background='white')

action_style.configure("general.Treeview", font=(font, 10))
action_style.configure("general.Treeview.Heading", font=(font, 12, 'bold'))
####### General Settings end here ###########


window.mainloop()