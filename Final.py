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
record_action = ['--', 'Midterm', 'Final Exam']

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

##### General functions ends here ######

def teacher_authenticate(login_frame,username_entry, password_entry):
    username = username_entry.get()
    password = password_entry.get()

    if not (8 <= len(username) <= 10) or not username.isdigit():
        messagebox.showerror("Staff Login", "Invalid user ID, you may not an admin try to login as a staff")
        return

    conn=db_connect()

    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM staff WHERE id = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            if result:
                # import staff
                # messagebox.showinfo("Staff Login", "Staff login successful!")
                # Pass user ID as a list containing the username converted to an integer
                login_frame.destroy()
                show_teacher_dashboard(result) #user data tuple is passed
                # window.destroy()
                # user_id = int(username)
                # staff.initiate(user_id)
            else:
                messagebox.showerror("Staff Login", "Invalid username or password.")
        except pymysql.Error as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")
        finally:
            conn.close()
    else:
        messagebox.showerror("Error", "Failed to connect to database.")

def admin_authenticate(loginframe,admin_username_entry, admin_password_entry):
    # Get username and password
    username = admin_username_entry.get()
    password = admin_password_entry.get()

    # Check if ID is an 8-digit integer
    if len(username) != 8 or not username.isdigit():
        messagebox.showerror("Admin Login", "Invalid user ID. Please enter an 8-digit ID number.")
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

    staffData_button = ttk.Button(Frame_adminBoard, text="Staff Data", command=lambda: show_staff_data(user),
                                    style='activeBtn.TButton', width=15)
    staffData_button.grid(row=1, column=0,columnspan=2, padx=5, pady=25,sticky='we')
    studentData_button = ttk.Button(Frame_adminBoard, text="Student Data", command=lambda: show_student_data(user),
                                  style='activeBtn.TButton', width=15)
    studentData_button.grid(row=2, column=0, columnspan=2, padx=5, pady=25, sticky='we')
    classSlot_button = ttk.Button(Frame_adminBoard, text="Class Slot", command=lambda: show_class_slot(user),
                                  style='activeBtn.TButton', width=15)
    classSlot_button.grid(row=3, column=0, columnspan=2, padx=5, pady=25, sticky='we')

def refresh_treetable(treetable,table):
    # Clear existing data from the Treeview widget
    treetable.delete(*treetable.get_children())

    # Repopulate the Treeview widget with the latest data from the database
    list=fetch_all_stud(table)
    for row in list:
        treetable.insert('', 'end', values=row)

### Teacher Dashboard ###

# def on_window_configure(event):
#     global action_frame
#     for frame in action_frame:
#         frame.place(x=0, y=window.winfo_height() * 0.1, width=window.winfo_width(),
#                     height=window.winfo_height() * 0.9)
def grade(marks):
    if marks >= 90:
        return 'A+'
    elif marks >= 80:
        return 'A'
    elif marks >= 70:
        return 'B+'
    elif marks >= 60:
        return 'B'
    elif marks >= 50:
        return 'C+'
    elif marks >= 40:
        return 'C'
    else:
        return 'F'

def bind_timeslot_combobox_event(timeSlot, selected_subject, frame):
    timeSlot.bind('<<ComboboxSelected>>', lambda event: fetch_students(selected_subject, frame))

def set_active_button(button):
    global action_btn

    for b in action_btn:
        if b == button:
            b.configure(style='activeBtn.TButton')
        else:
            b.configure(style='inactiveBtn.TButton')

def show_frame(frame):
    frame.tkraise()

def destroy_all_widgets(frame, obj):
    for widget in frame.winfo_children():
        if isinstance(widget, (ttk.Combobox)) or widget == obj:
            continue
        else:
            widget.destroy()

def bind_combobox_selection_event(class_sel, frame):
    class_sel.bind('<<ComboboxSelected>>', lambda event: fetch_time_slot(class_sel.get(), frame))
def fetch_time_slot(selected_subject, frame):
    connection =db_connect()

    destroy_all_widgets(frame, class_lbl)
    time_slots = []
    try:
        sql_time_slot = "SELECT ts.day, ts.start_time, ts.end_time FROM time_slot ts JOIN subject s ON ts.subject = s.code WHERE s.name = %s;"
        with connection.cursor() as cursor:
            cursor.execute(sql_time_slot, (selected_subject,))
            result_time_slot = cursor.fetchall()
            if result_time_slot:
                for slot in result_time_slot:
                    day, start_time, end_time = slot
                    time_slots.append(f"{day}: {start_time} - {end_time}")
            else:
                tk.messagebox.showerror("Error", "No time slot found for selected subject")
    except Exception as e:
        tk.messagebox.showerror("Error", f"Database error: {str(e)}")

    # Update the time slot dropdown menu
    timeSlot_lbl = ttk.Label(frame, text='Time Slot : ', style='edit.TLabel', background='white', padding=(40, 40))
    timeSlot_lbl.grid(row=0, column=2, sticky="e")
    timeSlot = ttk.Combobox(frame, values=time_slots, font=(font, '12'))
    timeSlot.grid(row=0, column=3, sticky="w", padx=20, pady=20)

    # Bind the timeslot combobox selection event
    bind_timeslot_combobox_event(timeSlot, selected_subject, frame)

def on_select(event,treeview,btn):
    selected_item = treeview.selection()
    if selected_item:
        values = treeview.item(selected_item, "values")
        student_id = values[1]  # Assuming the student ID is in the second column
        display_performance_report(student_id,btn)
    else:
        # Check if the selection is being cleared
        if event.widget.focus():
            tk.messagebox.showinfo("No Student Selected from table", "Please select a student from the table.")

def display_performance_report(student_id,btn):
    btn.configure(state='disabled')
    report_window = tk.Toplevel(window, bg='#F0E5F0', pady=20, padx=20)
    report_window.title("Performance Report")
    report_window.geometry(f"+300+80")

    fetch_user(student_id, 'student')
    row = 1
    for field, value in stud_info.items():
        value = str(value)
        if field == 'profile_pic':
            load_profilePic(report_window, 80, 80, value)
        elif field == 'annual_review' or field == 'subject' or field == 'year':
            pass
        else:
            ttk.Label(report_window, text=field.capitalize() + ":", style='edit.TLabel').grid(row=row, column=0,
                                                                                              padx=10,
                                                                                              pady=5, sticky="w")
            ttk.Label(report_window, text=value, style='edit.TLabel', font=('normal')).grid(
                row=row, column=1, padx=10,
                pady=5, sticky="w")

            row += 1
    ttk.Label(report_window, text="Year: " + str(stud_info['year']), style='edit.TLabel').grid(row=0, column=4,
                                                                                               columnspan=2,
                                                                                               padx=20, pady=20,
                                                                                               sticky='w')

    report_detail = ttk.LabelFrame(report_window, text='Academic Report', style='edit.TLabelframe')
    report_detail.grid(row=1, rowspan=row - 1, column=4, columnspan=2, padx=20, pady=20)
    ttk.Label(report_detail, text="No.", style='edit.TLabel').grid(row=1, column=0)
    ttk.Label(report_detail, text="Subject", style='edit.TLabel').grid(row=1, column=1)
    ttk.Label(report_detail, text="Midterm", style='edit.TLabel').grid(row=1, column=2)
    ttk.Label(report_detail, text="Final Exam", style='edit.TLabel').grid(row=1, column=3)
    ttk.Label(report_detail, text="Grade", style='edit.TLabel').grid(row=1, column=4)
    ttk.Label(report_detail, text="Attendance(%)", style='edit.TLabel').grid(row=1, column=5)
    separator = ttk.Separator(report_detail, orient='horizontal')
    separator.grid(row=2, column=0, columnspan=6, sticky='ew')

    ttk.Label(report_window, text="Form Teacher Comment:", style='edit.TLabel').grid(row=row, column=4,
                                                                                     columnspan=2, padx=20, pady=20,
                                                                                     sticky='w')
    comment_entry = ttk.Entry(report_window, style='edit.TEntry')
    comment_entry.insert(0, stud_info['annual_review'])
    comment_entry.grid(row=row, column=5, columnspan=2, padx=20, pady=20, sticky='we')

    i = 1
    counter = 3
    atten_count = []
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='tintots_kindergarden'
    )
    cursor = connection.cursor()
    try:
        sql = "SELECT * FROM marks_record WHERE stud_id = %s;"
        cursor.execute(sql, int(student_id, ))
        subject_marks = cursor.fetchall()
        if subject_marks:
            for itm in subject_marks:
                sub = itm[1]
                midterm = itm[4]
                final = itm[5]

                sql_attendance = "SELECT * FROM attendance_record WHERE subject = %s AND stud_id = %s;"
                cursor.execute(sql_attendance, (sub, student_id))
                subject_attend = cursor.fetchall()
                if subject_attend:
                    for att in subject_attend:
                        atten_count.append(att[-1])

                ttk.Label(report_detail, text=str(i), style='edit.TLabel').grid(row=counter, column=0)
                ttk.Label(report_detail, text=str(sub), style='edit.TLabel').grid(row=counter, column=1)
                ttk.Label(report_detail, text=str(midterm), style='edit.TLabel').grid(row=counter, column=2)
                ttk.Label(report_detail, text=str(final), style='edit.TLabel').grid(row=counter, column=3)
                ttk.Label(report_detail, text=str(grade((midterm + final) / 2)), style='edit.TLabel').grid(
                    row=counter, column=4)
                # Handle division by zero when calculating attendance percentage
                attendance_percentage = (atten_count.count(0) / len(atten_count) * 100) if len(
                    atten_count) != 0 else 0
                ttk.Label(report_detail, text='{}%'.format(round(attendance_percentage)), style='edit.TLabel').grid(
                    row=counter, column=5)
                i += 1
                counter += 1
        else:
            tk.messagebox.showerror("Error", "Student does not take any subject")
    except Exception as e:
        tk.messagebox.showerror("Error", f"Database error: {str(e)}")

    def submit_close(stud_id):
        try:
            sql = "UPDATE student SET annual_review = %s WHERE id = %s;"
            cursor.execute(sql, (comment_entry.get(), stud_id))
            connection.commit()
            report_window.destroy()  # Close the report window
            btn.configure(state='normal')
        except Exception as e:
            tk.messagebox.showerror("Error", f"Database error: {str(e)}")

    def download_report():
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if filename:
                c = canvas.Canvas(filename, pagesize=letter)
                # Set the font and size for the content
                c.setFont("Helvetica", 12)
                y_position = 750  # Initial y position for the content

                # Write the content from the report window to the PDF
                for widget in report_window.winfo_children():
                    if isinstance(widget, ttk.Label):
                        c.drawString(100, y_position, widget.cget("text"))
                        y_position -= 20  # Adjust the y position for the next content
                    elif isinstance(widget, ttk.LabelFrame):
                        # Draw LabelFrame title
                        c.drawString(100, y_position, widget.cget("text"))
                        y_position -= 20  # Adjust the y position for the next content
                        # Draw LabelFrame content
                        for child_widget in widget.winfo_children():
                            if isinstance(child_widget, ttk.Label):
                                c.drawString(120, y_position, child_widget.cget("text"))
                                y_position -= 20  # Adjust the y position for the next content
                c.save()
                tk.messagebox.showinfo("Success", f"Report downloaded as {filename}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to download report: {str(e)}")

    done_button = ttk.Button(report_window, text="Done", style='actionBtn.TButton',
                             command=lambda: submit_close(student_id))
    done_button.grid(row=row + 1, column=4, padx=20, sticky='e')
    download_button = ttk.Button(report_window, text="Download", style='actionBtn.TButton', command=download_report)
    download_button.grid(row=row + 1, column=5, padx=20, sticky='e')

def profile_clicked(user,button):
    set_active_button(button)
    ### FRAME 1
    Frame_profile = tk.Frame(window, bd=5, relief=tk.FLAT, bg="white")
    Frame_profile.place(x=0, y=window.winfo_height() * 0.1, width=window.winfo_width(),
                     height=window.winfo_height() * 0.9)
    Frame_profile.tkraise()
    user_id=user[0]
    display_userPic(Frame_profile, 180, 180, user_id,'staff')
    Editprofile_button = ttk.Button(Frame_profile, text="Edit Profile", command=lambda: edit_profile(),
                                    style='actionBtn.TButton', width=15)
    Editprofile_button.grid(row=1, column=0, padx=5, pady=5)
    profile_lblframe = ttk.LabelFrame(Frame_profile, text='PROFILE', style='general.TLabelframe')
    profile_lblframe.grid(row=0, column=1, padx=5, sticky="nsew")
    Frame_profile.columnconfigure(1, weight=1)
    empty_lblframe = tk.Label(profile_lblframe, padx=30, bg='white')
    empty_lblframe.grid(row=0, column=2, padx=5, sticky="nsew")
    row = 0

    display_user_data(profile_lblframe)

    ttk.Label(Frame_profile, text="Qualification", style='edit.TLabel', background='white').grid(row=1, column=1,
                                                                                                 padx=10,
                                                                                                 pady=5, sticky="w")
    # Create a Text widget for displaying the content
    content_text = tk.Text(Frame_profile, wrap="word", font=(font, 12), borderwidth=0, highlightthickness=0)
    content_text.grid(row=2, column=1, sticky="nsew")

    # Create a vertical scrollbar
    qualification = tk.Scrollbar(Frame_profile, orient="vertical", command=content_text.yview, borderwidth=0,
                                 highlightthickness=0)
    qualification.grid(row=3, column=1, sticky="nsew")
    content_text.config(yscrollcommand=qualification.set)

    # Insert the content text into the Text widget
    content_text.insert("1.0", user_info['qualification'])
    content_text.config(state="disabled")

def attendance_clicked(user,button):
    set_active_button(button)
    # FRAME 2
    Frame_attendance = tk.Frame(window, bd=5, relief=tk.FLAT, bg="white")
    action_frame.append(Frame_attendance)
    Frame_attendance.columnconfigure(1, weight=1)
    teach_subject(user, Frame_attendance, attendance_frame=Frame_attendance)

def assessment_clicked(user,button):
    set_active_button(button)
    # FRAME 3
    Frame_assessment = tk.Frame(window, bd=5, relief=tk.FLAT, bg="white")
    action_frame.append(Frame_assessment)

    teach_subject(user, Frame_assessment, assessment_frame=Frame_assessment)

def report_clicked(user,button):
    set_active_button(button)

    # FRAME 4 -Report, only available to form teacher
    Frame_report = tk.Frame(window, bd=5, relief=tk.FLAT, bg="white")
    action_frame.append(Frame_report)
    Frame_report.columnconfigure(1, weight=1)

    search_entry = ttk.Entry(Frame_report, width=30, style='edit.TEntry')
    search_entry.grid(row=0, column=3, padx=10, pady=10, sticky='e')

    # Table to display student information
    columns = ("No.", "Student ID", "Student Name")
    student_tree = ttk.Treeview(Frame_report, columns=columns, show="headings", style="general.Treeview")
    for col in columns:
        student_tree.heading(col, text=col, anchor="center")
    student_tree.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky='nsew')

    # Bind the on_select function to the Treeview widget
    student_tree.bind("<<TreeviewSelect>>", lambda event: on_select(event, student_tree,view_button))

    view_button = ttk.Button(Frame_report, text="View", command=lambda :view_performance_report(student_tree,view_button), style='activeBtn.TButton', )
    view_button.grid(row=2, column=3, padx=10, pady=10, sticky='e')

    refresh_treetable(student_tree,'student')

def view_performance_report(treeview,btn):
    selected_item = treeview.selection()
    if selected_item:
        values = treeview.item(selected_item, "values")
        student_id = values[1]  # Assuming the student ID is in the second column
        display_performance_report(student_id,btn)
    else:
        tk.messagebox.showinfo("No Student Selected from view button", "Please select a student from the table.")

def teach_subject(user, frame, assessment_frame=None, attendance_frame=None):
    conn=db_connect()
    global class_lbl
    subjects = []
    try:
        sql = "SELECT c.name FROM subject c JOIN staff s ON c.assigned = s.id WHERE s.id = %s;"
        with conn.cursor() as cursor:
            cursor.execute(sql, (user,))
            result = cursor.fetchall()
            if result:
                for subject in result:
                    subjects.append(subject[0])
            else:
                tk.messagebox.showerror("Error", "User not found in the database")
                return

        class_lbl = ttk.Label(frame, text='Class : ', style='edit.TLabel', background='white', padding=(40, 40))
        class_lbl.grid(row=0, column=0, sticky="e")
        class_sel = ttk.Combobox(frame, values=subjects, font=(font, '12'))
        class_sel.grid(row=0, column=1, sticky="w", padx=20, pady=20)

        # Bind the class combobox selection event
        bind_combobox_selection_event(class_sel, frame)

        if frame == assessment_frame:
            class_lbl = ttk.Label(frame, text='Subject : ', style='edit.TLabel', background='white',
                                  padding=(40, 40))
            class_lbl.grid(row=0, column=0, sticky="e")
            class_sel.bind('<<ComboboxSelected>>', lambda event: record_marks(class_sel.get(), frame))
            destroy_all_widgets(frame, None)
            return
        elif frame == attendance_frame:
            class_sel.bind('<<ComboboxSelected>>', lambda event: fetch_time_slot(class_sel.get(), frame))

    except Exception as e:
        tk.messagebox.showerror("Error", f"Database error: {str(e)}")
        return

def record_marks(selected_subject, frame):
    global row_count
    connection =db_connect()
    ttk.Label(frame, text="No.", style='heading.TLabel').grid(row=1, column=0)
    ttk.Label(frame, text="Student ID", style='heading.TLabel').grid(row=1, column=1)
    ttk.Label(frame, text="Student Name", style='heading.TLabel').grid(row=1, column=2)
    ttk.Label(frame, text="Midterm", style='heading.TLabel').grid(row=1, column=3)
    ttk.Label(frame, text="Final Exam", style='heading.TLabel').grid(row=1, column=4)
    separator = ttk.Separator(frame, orient='horizontal')
    separator.grid(row=2, column=0, columnspan=5, sticky='ew')
    i = 1
    row_count = 3
    entries_midterm = []
    entries_final = []

    try:
        sql = "SELECT stud_id, stud_name , midterm, final FROM marks_record WHERE subject = %s;"
        with connection.cursor() as cursor:
            cursor.execute(sql, (selected_subject,))
            result = cursor.fetchall()
            if result:
                for slot in result:
                    ttk.Label(frame, text=str(i), style='general.TLabel').grid(row=row_count, column=0)
                    ttk.Label(frame, text=slot[0], style='general.TLabel').grid(row=row_count, column=1)
                    ttk.Label(frame, text=slot[1], style='general.TLabel').grid(row=row_count, column=2)
                    entry_midterm = ttk.Entry(frame, style='edit.TEntry')
                    entry_midterm.insert(0, slot[2])
                    entry_midterm.grid(row=row_count, column=3)
                    entry_midterm.config(state='disabled')
                    entries_midterm.append(entry_midterm)

                    entry_final = ttk.Entry(frame, style='edit.TEntry')
                    entry_final.insert(0, slot[3])
                    entry_final.grid(row=row_count, column=4)
                    entry_final.config(state='disabled')
                    entries_final.append(entry_final)

                    i += 1
                    row_count += 1

            else:
                tk.messagebox.showerror("Error", "No student found for selected subject")
    except Exception as e:
        tk.messagebox.showerror("Error", f"Database error: {str(e)}")

    def update_entry_state(event):
        action = recordAction.get()
        if action == "Midterm":
            for entry in entries_midterm:
                entry.config(state='normal')
            for entry in entries_final:
                entry.config(state='disabled')
        elif action == "Final Exam":
            for entry in entries_midterm:
                entry.config(state='disabled')
            for entry in entries_final:
                entry.config(state='normal')

    def save_records():
        try:
            with connection.cursor() as cursor:
                for idx, (stud_id, _, _, _) in enumerate(result):
                    midterm = entries_midterm[idx].get()
                    final_exam = entries_final[idx].get()
                    sql_update = "UPDATE marks_record SET midterm = %s, final = %s WHERE stud_id = %s AND subject = %s;"
                    cursor.execute(sql_update, (midterm, final_exam, stud_id, selected_subject))
                connection.commit()
                tk.messagebox.showinfo("Success", "Records saved successfully!")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Database error: {str(e)}")

    recordAction_lbl = ttk.Label(frame, text='Record Marks for : ', style='edit.TLabel', background='white',
                                 padding=(40, 40))
    recordAction_lbl.grid(row=0, column=2, sticky="e")
    recordAction = ttk.Combobox(frame, values=record_action, font=(font, '12'))
    recordAction.grid(row=0, column=3, sticky="w", padx=20, pady=20)
    recordAction.bind('<<ComboboxSelected>>', update_entry_state)

    record_button = ttk.Button(frame, text="Record", command=save_records, style='actionBtn.TButton')
    record_button.grid(row=row_count + 2, columnspan=5, padx=5, pady=5, sticky="se")

def fetch_students(selected_subject, frame):
    destroy_all_widgets(frame, class_lbl)
    global row_count
    connection = db_connect()
    subj_student = {}
    cursor = connection.cursor()
    try:
        # Fetch the year of the selected subject
        sql_subject_year = "SELECT year FROM subject WHERE name = %s;"
        cursor.execute(sql_subject_year, (selected_subject,))
        subject_year = cursor.fetchone()
        if subject_year:
            # Fetch students whose year matches the year of the selected subject
            sql_students = "SELECT id, name FROM student WHERE year = %s;"
            cursor.execute(sql_students, (subject_year,))
            result_students = cursor.fetchall()
            if result_students:
                for student in result_students:
                    subj_student[student[0]] = student[1]
            else:
                tk.messagebox.showerror("Error", "No students found for the selected subject")
        else:
            tk.messagebox.showerror("Error", "Year not found for the selected subject")
    except Exception as e:
        tk.messagebox.showerror("Error", f"Database error: {str(e)}")

    ttk.Label(frame, text="No.", style='heading.TLabel').grid(row=1, column=0)
    ttk.Label(frame, text="Student ID", style='heading.TLabel').grid(row=1, column=1)
    ttk.Label(frame, text="Student Name", style='heading.TLabel').grid(row=1, column=2)
    ttk.Label(frame, text="Attendance", style='heading.TLabel').grid(row=1, column=3)
    separator = ttk.Separator(frame, orient='horizontal')
    separator.grid(row=2, column=0, columnspan=4, sticky='ew')
    attendance_data = {}
    if row_count == 0:
        row_count = 3
    for i, (student_id, student_name) in enumerate(subj_student.items(), start=1):
        ttk.Label(frame, text=str(i), style='general.TLabel').grid(row=row_count, column=0)
        ttk.Label(frame, text=str(student_id), style='general.TLabel').grid(row=row_count, column=1)
        ttk.Label(frame, text=str(student_name), style='general.TLabel').grid(row=row_count, column=2)
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(frame, variable=var)
        checkbox.grid(row=row_count, column=3)
        attendance_data[student_id] = var
        row_count += 1

    submit_button = ttk.Button(frame, text="Submit",
                               command=lambda: submit_attendance(attendance_data, subj_student, selected_subject,
                                                                 submit_button,frame), style='actionBtn.TButton')
    submit_button.grid(row=row_count + 3, columnspan=5, pady='20', padx='20', sticky="e")
    connection.close()

def submit_attendance(attendance_data, subj_student, selected_subject, submit_btn,frame):
    connection = db_connect()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with connection.cursor() as cursor:
            for student_id, var in attendance_data.items():
                student_name = subj_student[student_id]
                attendance = 1 if var.get() else 0
                sql = "INSERT INTO attendance_record (subject, stud_id, student, time_recorded, attendance) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (selected_subject, student_id, student_name, current_time, attendance))
            connection.commit()
            messagebox.showinfo("Success", "Attendance recorded successfully!")
            frame.destroy()

    except Exception as e:
        messagebox.showerror("Error", f"Database error: {str(e)}")

def show_teacher_dashboard(user):
    global action_frame, action_btn,user_info
    # Clear existing widgets from the parent frame
    for widget in window.winfo_children():
        widget.destroy()
    # window.bind('<Configure>', on_window_configure)

    user_id = user[0]
    user_info = fetch_user(user_id, 'staff')
    ### FRAME ###
    ### NAVI
    Frame_buttonNav = tk.Frame(window, bd=5, relief=tk.FLAT, bg="#F0E5F0")
    Frame_buttonNav.place(x=0, y=0, width=window.winfo_width(), height=window.winfo_height() * 0.1)

    profile_button = ttk.Button(Frame_buttonNav, text="Profile", command=lambda: profile_clicked(user,profile_button), style='inactiveBtn.TButton',
                                width=15)
    profile_button.grid(row=0, column=0, padx=5)
    action_btn.append(profile_button)

    attendance_button = ttk.Button(Frame_buttonNav, text="Attendance", command=lambda :attendance_clicked(user,attendance_button),
                                   style='inactiveBtn.TButton', width=15)
    attendance_button.grid(row=0, column=1, padx=5)
    action_btn.append(attendance_button)

    assessment_button = ttk.Button(Frame_buttonNav, text="Assessment", command=lambda:assessment_clicked(user,assessment_button),
                                   style='inactiveBtn.TButton', width=15)
    assessment_button.grid(row=0, column=2, padx=5)
    action_btn.append(assessment_button)

    report_button = ttk.Button(Frame_buttonNav, text="Report", command=lambda: report_clicked(user,report_button), style='inactiveBtn.TButton',
                               width=15)
    report_button.grid(row=0, column=4, padx=5)
    action_btn.append(report_button)
    # position = get_staff_position(user)

    # if position == 'form teacher':
    #     action_btn.append(report_button)
    # else:
    #     report_button.grid_remove()

    exit_icon = Image.open("logout.png")
    exit_icon = exit_icon.resize((25, 25), Image.LANCZOS)
    exit_icon = ImageTk.PhotoImage(exit_icon)
    exit_button = ttk.Button(Frame_buttonNav, image=exit_icon, text="Exit", command=logout(),
                             style='activeBtn.TButton')
    exit_button.grid(row=0, column=5, sticky="e")
    # Configure column weights to distribute space evenly
    Frame_buttonNav.grid_columnconfigure((0, 1, 2, 3), weight=1)
    Frame_buttonNav.grid_columnconfigure(4, weight=2)

    # profile_clicked(user,profile_button)

### Teacher DashBoard ends here ###

### Staff Data ###
def show_staff_data(user):
    global all_stud
    # Clear existing widgets from the parent frame
    for widget in window.winfo_children():
        widget.destroy()

    all_stud=fetch_all_stud('staff')
    back_button = ttk.Button(window, style='activeBtn.TButton', text='Back', command=lambda: admin_main_interface(user))
    back_button.place(x=10, y=10)

    # Left frame for data entry
    left_frame = tk.Frame(window, bg='white', pady=10, padx=10)
    left_frame.place(x=0, y=50, width=int(window.winfo_width() * 0.30), height=int(window.winfo_height() - 30))

    right_frame = tk.Frame(window, bg='#F0E5F0')
    right_frame.place(x=int(window.winfo_width() * 0.25), y=0, width=int(window.winfo_width() * 0.75),
                      height=int(window.winfo_height()))
    right_frame.columnconfigure(0, weight=1)
    right_frame.columnconfigure(1, weight=1)
    right_frame.grid_rowconfigure(1, weight=1)

    global search_entry

    search_entry = ttk.Entry(right_frame, width=30, style='edit.TEntry')
    search_entry.grid(row=0, column=0, padx=10, pady=10, sticky='e')
    # Create the search button
    search_button = ttk.Button(right_frame, text="Search", style='actionBtn.TButton',command=lambda: search_students(staff_listbox,all_stud,'staff') )
    search_button.grid(row=0, column=1, padx=10, pady=10, sticky='w')

    # Labels for staff details entry
    staff_labels = ["ID", "Name", "Contact", "Password", "Age", "Address",
                    "Email", "Qualification", "Position", "Department", "Salary"]

    # Entry fields for staff details
    entry_fields = {}
    for i, label in enumerate(staff_labels):
        ttk.Label(left_frame, text=label, style='general.TLabel').grid(row=i, column=0, padx=10, pady=5)
        entry_fields[label.lower()] = ttk.Entry(left_frame,style='edit.TEntry')
        entry_fields[label.lower()].grid(row=i, column=1, padx=10, pady=5)

    # Profile pic selection button
    profile_pic_var = tk.StringVar()
    profile_pic_label = ttk.Label(left_frame, text="Profile Picture", style='general.TLabel')
    profile_pic_label.grid(row=len(staff_labels) + 1, column=0, padx=10, pady=5)
    profile_pic_button = ttk.Button(left_frame, text="Select Profile Picture",
                                    command=lambda: select_profile_pic(profile_pic_var), style='Btn.TButton')
    profile_pic_button.grid(row=len(staff_labels) + 1, column=1, padx=10, pady=5)

    add_button = ttk.Button(left_frame, text="ADD",
                            command=lambda: save_staff_data(entry_fields, profile_pic_var, staff_listbox),
                            style='activeBtn.TButton')
    add_button.grid(row=len(staff_labels) + 2, column=0, padx=2, pady=2, sticky="we")

    # Clear fields button
    clear_btn = ttk.Button(left_frame, text="CLEAR",
                           command=lambda: clear_fields(entry_fields, add_button, edit_button, delete_button,
                                                        clear_btn),
                           style='activeBtn.TButton')
    clear_btn.grid(row=len(staff_labels) + 3, column=0, padx=2, pady=2, sticky="we")

    edit_button = ttk.Button(left_frame, text="UPDATE", command=lambda: update_staff(entry_fields, staff_listbox),
                             style='activeBtn.TButton')
    edit_button.grid(row=len(staff_labels) + 3, column=1, padx=2, pady=2, sticky="we")

    # Delete button
    delete_button = ttk.Button(left_frame, text="DELETE",
                               command=lambda: delete_staff_data(staff_listbox),
                               style='activeBtn.TButton')
    delete_button.grid(row=len(staff_labels) + 2, column=1, padx=2, pady=2, sticky="we")

    add_button['state'] = 'enabled'
    edit_button['state'] = 'disabled'
    delete_button['state'] = 'disabled'
    clear_btn['state'] = 'enabled'

    # Staff listbox
    staff_listbox = ttk.Treeview(right_frame, columns=staff_labels, show="headings",style="general.Treeview")
    for col in staff_labels:
        staff_listbox.heading(col, text=col, anchor=tk.CENTER)
        staff_listbox.column(col, width=80)
    staff_listbox.grid(row=1, columnspan=2,padx=10, pady=10, sticky='nsew')
    for row in all_stud:
        staff_listbox.insert("", "end", values=row)
    staff_listbox.bind("<<TreeviewSelect>>", lambda event: propagate_selected_row(event,staff_listbox,staff_labels,entry_fields, add_button, edit_button, delete_button, clear_btn))

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
                refresh_treetable(staff_treeview,'staff')
    else:
        messagebox.showwarning("No Selection", "Please select a staff data to delete.")

def save_staff_data(entries, profile_pic_var, staff_treeview):
    # Retrieve data from entry fields
    # id = entries["id"].get()
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
        query = "INSERT INTO staff (name, contact, password, age, address, email, qualification, position, department, salary, profile_pic) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (
            name, contact, password, age, address, email, qualification, position, department, salary,
            profile_pic))
        # Show confirmation message
        confirm = messagebox.askyesno("Confirm Saved", "Are you sure you want to save this staff data?")
        if confirm:
            conn.commit()
            messagebox.showinfo("Success", "Staff data saved successfully.")
            # Refresh the staff list after saving
            refresh_treetable(staff_treeview,'staff')
            # Clear entry fields after saving
            for entry in entries.values():
                entry.delete(0, tk.END)

def update_staff(entries, treeview):
    # Get the updated data from entry fields
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

    conn = db_connect()
    if conn:
        cursor = conn.cursor()
        try:
            # Construct the SQL query to update the student details
            query = """
                    UPDATE staff 
                    SET name = %s, contact = %s, password = %s, age = %s, address = %s,
                        email = %s, qualification = %s, position = %s, department = %s, salary = %s
                    WHERE id = %s;
                    """
            # Execute the query
            cursor.execute(query, (name,contact,password,age,address,email,qualification,position,department,salary , id))
            # Commit changes to the database
            conn.commit()
            messagebox.showinfo("Success", "Student data saved successfully.")

            # Refresh the student listbox
            refresh_treetable(treeview,'staff')
        except pymysql.Error as e:
            messagebox.showinfo("Error", "Staff data saved unsuccessfully.")
            # Rollback changes in case of error
            conn.rollback()
        finally:
            # Close cursor and connection
            cursor.close()
            conn.close()

### Staff Data Ends here ###

### Show Student Data ###

def fetch_all_stud(table):
    connection = pymysql.connect(host='localhost',user='root',password='',database='tintots_kindergarden')
    cursor = connection.cursor()
    try:
        sql = f"SELECT * FROM {table} ;"
        cursor.execute(sql)
        all_stud = cursor.fetchall()
        if all_stud:
            for row in all_stud:
                all_student_IdName[row[0]] = row[1]
        else:
            tk.messagebox.showerror("Error", "No Student Found!")
        return all_stud  # Return the value of all_stud
    except Exception as e:
        tk.messagebox.showerror("Error", f"Database error: {str(e)}")

def search_students(treetable,list,table):
    search_text = search_entry.get()

    if not search_text:
        # If search text is empty, reset the tree to show all items
        refresh_treetable(treetable,table)
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
            tk.messagebox.showinfo("No Student Found", "No matching for the search criteria was found.")

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
            refresh_treetable(treetable,'student')

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
            refresh_treetable(treetable,'student')
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
                refresh_treetable(student_listbox,'student')
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
            refresh_treetable(student_treeview,'student')
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

    all_stud = fetch_all_stud('student')

    back_button=ttk.Button(window,style='activeBtn.TButton',text='Back',command=lambda: admin_main_interface(user))
    back_button.place(x=10,y=10)

    # Left frame for data entry
    left_frame = tk.Frame(window,bg='white', pady=10, padx=10)
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
    search_button = ttk.Button(right_frame, text="Search", style='actionBtn.TButton',command=lambda: search_students(student_treeview,all_stud,'student') )
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

window = tk.Tk()
screen_width = window.winfo_screenwidth() * 0.99
screen_height = window.winfo_screenheight()* 0.99
window.geometry(f"{int(screen_width)}x{int(screen_height)}+0+0")
window.title("Tintots Kindergarden")
window.configure(bg="#f0e5f0")


def login():
    global user_info, stud_info, all_student_IdName, all_stud, profile_ctrlRow, searching,add_button,edit_button,delete_button,clear_btn
    global action_teacher_btn,action_teacher_frame
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

    action_teacher_btn = []
    action_teacher_frame = []

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
    admin_button = ttk.Button(login_frame, text="Admin Login", style="activeBtn.TButton",width=20, command=lambda: admin_authenticate(login_frame,username_entry, password_entry))
    admin_button.grid(row=3, columnspan=2,pady=10)

    # Teacher login button
    staff_button = ttk.Button(login_frame, text="Teacher Login",  style="activeBtn.TButton",width=20,command=lambda: teacher_authenticate(login_frame,username_entry, password_entry))
    staff_button.grid(row=4, columnspan=2,pady=10)

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