import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import pymysql
from PIL import Image, ImageTk
from datetime import datetime
from tkinter import filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

user=1
font='Lato'

# subjects=["Bahasa Melayu","English","Mathematics","Science","Living Skills","Physical Education","Art","Music"]
subjects=[]
subj_student={}
time_slot=[]
user_info={}
stud_info={}
record_action=['--','Midterm','Final Exam']
record_action_list=[]

### database conn ##
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='tintots_kindergarden'
)

### FUNCTION ###
def go_back():
    pass


def on_window_configure(event):
    Frame_buttonNav.place(x=0, y=0, width=window.winfo_width(), height=window.winfo_height()*0.1)
    for frame in action_frame:
        frame.place(x=0, y=window.winfo_height() * 0.1, width=window.winfo_width(),
                            height=window.winfo_height() * 0.9)

#----- General Functions -----#
def set_active_button(button):
    for b in action_btn:
        if b == button:
            b.configure(style='activeBtn.TButton')
        else:
            b.configure(style='inactiveBtn.TButton')

def show_frame(frame):
    frame.tkraise()

# Define button click actions
def profile_clicked():
    show_frame(Frame_profile)
    set_active_button(profile_button)

def attendance_clicked():
    show_frame(Frame_attendance)
    set_active_button(attendance_button)
    teach_subject(user, Frame_attendance, attendance_frame=Frame_attendance)

def assessment_clicked():
    show_frame(Frame_assessment)
    set_active_button(assessment_button)
    teach_subject(user, Frame_assessment, assessment_frame=Frame_assessment)

def report_clicked():
    show_frame(Frame_report)
    set_active_button(report_button)

def destroy_all_widgets(frame,obj):
    for widget in frame.winfo_children():
        if isinstance(widget, (ttk.Combobox)) or widget == obj:
            continue
        else:
            widget.destroy()


#-----END-----#

#----- Specialized Functions -----#

def get_staff_position(user):
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='tintots_kindergarden'
        )
        with connection.cursor() as cursor:
            # Retrieve the position for the given user
            sql = "SELECT position FROM staff WHERE name = %s;"
            cursor.execute(sql, (user,))
            result = cursor.fetchone()
            if result:
                # Return the position
                return result[0]
            else:
                return None  # User not found
    except Exception as e:
        tk.messagebox.showerror("Error", f"Database error: {str(e)}")


# Function to display the image in the frame
def display_userPic(frame, width, height, user):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT profile_pic FROM staff WHERE id=%s;"
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
        load_profilePic(frame, width, height, image_path)

def load_profilePic(frame, width, height,image_path):
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
    label.grid(row=0, column=0, padx=15,pady=15)


def submit_attendance(attendance_data, subj_student,selected_subject,submit_btn):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='tintots_kindergarden'
    )
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
            submit_btn.destroy()
            destroy_all_widgets(Frame_attendance,None)
            teach_subject(user, Frame_attendance)
    except Exception as e:
        messagebox.showerror("Error", f"Database error: {str(e)}")

row_count = 0
def fetch_students(selected_subject, frame):
    destroy_all_widgets(frame, class_lbl)
    global row_count
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='tintots_kindergarden'
    )
    subj_student = {}
    cursor = connection.cursor()
    try:
        # Fetch the year of the selected subject
        sql_subject_year = "SELECT year FROM subject WHERE name = %s;"
        cursor.execute(sql_subject_year, (selected_subject,))
        subject_year = cursor.fetchone()
        if subject_year:
            # Fetch students whose year matches the year of the selected subject
            sql_students = "SELECT id, name FROM stud_ms WHERE year = %s;"
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



    submit_button = ttk.Button(frame, text="Submit", command=lambda: submit_attendance(attendance_data, subj_student,selected_subject,submit_button), style='actionBtn.TButton')
    submit_button.grid(row=row + 3, columnspan=5, pady='20', padx='20', sticky="e")
    connection.close()


def fetch_user(user,table):
    global user_info
    user_info = {}
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='tintots_kindergarden'
    )
    try:
        sql = f"SELECT * FROM {table} WHERE id=%s;"
        with connection.cursor() as cursor:
            cursor.execute(sql, (user,))
            result = cursor.fetchone()
            if result:
                if table=='staff':
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
                elif table=='stud_ms':
                    stud_info['id'] = result[0]
                    stud_info['name'] = result[1]
                    stud_info['age'] = result[2]
                    stud_info['contact'] = result[3]
                    stud_info['address'] = result[4]
                    stud_info['enrol_date'] = result[5]
                    stud_info['year'] = result[6]
                    stud_info['subject'] = result[7]
                    stud_info['annual_review'] = result[8]
                    stud_info['profile_pic'] = result[9]
            else:
                tk.messagebox.showerror("Error", "User not found.")
                return

    except Exception as e:
        tk.messagebox.showerror("Error", f"Database error: {str(e)}")
        return


def edit_profile(user):
    fetch_user(user,'staff')
    # Create a pop-up window for editing
    edit_window = tk.Toplevel(Frame_profile,bg='#F0E5F0')
    edit_window.title("Edit Profile")
    edit_window.geometry(f"+300+150")
    edit_detail = ttk.LabelFrame(edit_window, style='edit.TLabelframe')
    edit_detail.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Entry widgets to display and edit user info
    entries = {}
    row = 0
    for field, value in user_info.items():
        if field in ["id" , "name" , "password" , "email" , "contact","address"]:
            ttk.Label(edit_detail, text=field.capitalize() + ":", style='edit.TLabel').grid(row=row, column=0, padx=5,
                                                                                            pady=10, sticky="w")
            entry = ttk.Entry(edit_detail, style='edit.TEntry')
            entry.insert(0, value)
            entry.grid(row=row, column=1, padx=10, pady=10, sticky="w")
            entries[field] = entry
            if field == "id":
                entry.config(state="readonly")

            row += 1

    def save_changes(user_info):
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='tintots_kindergarden'
        )
        # Function to save the changes made by the user
        new_name = entries['name'].get()
        new_password = entries['password'].get()
        new_email = entries['email'].get()
        new_contact = entries['contact'].get()
        new_address = entries['address'].get()
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE staff SET name=%s, contact=%s, password=%s,  address=%s, email=%s WHERE id=%s;"
                print(sql, (new_name, new_contact,new_password,  new_address,new_email, user_info['id']))
                cursor.execute(sql, (new_name, new_contact,new_password,  new_address,new_email, user_info['id']))
                connection.commit()
                edit_window.destroy()
                tk.messagebox.showinfo("Success", "Profile updated successfully")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Database error: {str(e)}")
            edit_window.destroy()



    # Button to save changes
    save_button = ttk.Button(edit_detail, text="Save Changes", command=lambda: save_changes(user_info), style='actionBtn.TButton')
    save_button.grid(row=row, column=0, columnspan=2, padx=5, pady=10)

def record_marks(selected_subject, frame):
    global row_count
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='tintots_kindergarden'
    )
    ttk.Label(frame, text="No.", style='heading.TLabel').grid(row=1, column=0)
    ttk.Label(frame, text="Student ID", style='heading.TLabel').grid(row=1, column=1)
    ttk.Label(frame, text="Student Name", style='heading.TLabel').grid(row=1, column=2)
    ttk.Label(frame, text="Midterm", style='heading.TLabel').grid(row=1, column=3)
    ttk.Label(frame, text="Final Exam", style='heading.TLabel').grid(row=1, column=4)
    separator = ttk.Separator(frame, orient='horizontal')
    separator.grid(row=2, column=0, columnspan=5, sticky='ew')
    i=1
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

    record_button = ttk.Button(frame, text="Record", command=save_records,style='actionBtn.TButton')
    record_button.grid(row=row_count+2, columnspan=5, padx=5, pady=5, sticky="se")


# def teach_subject(user, frame, assessment_frame=None, attendance_frame=None):
#     connection = pymysql.connect(
#         host='localhost',
#         user='root',
#         password='',
#         database='tintots_kindergarden'
#     )
#     global class_lbl
#     subjects = []
#     try:
#         sql = "SELECT c.name FROM subject c JOIN staff s ON c.assigned = s.id WHERE s.id = %s;"
#         with connection.cursor() as cursor:
#             cursor.execute(sql, (user,))
#             result = cursor.fetchall()
#             if result:
#                 for subject in result:
#                     subjects.append(subject[0])
#             else:
#                 tk.messagebox.showerror("Error", "User not found in the database")
#                 return
#
#         class_lbl = ttk.Label(frame, text='Class : ', style='edit.TLabel', background='white',
#                                  padding=(40, 40))
#         class_lbl.grid(row=0, column=0, sticky="e")
#         class_sel = ttk.Combobox(frame, values=subjects, font=(font, '12'))
#         class_sel.grid(row=0, column=1, sticky="w", padx=20, pady=20)
#
#         if frame == assessment_frame:
#             class_sel.bind('<<ComboboxSelected>>', lambda event: record_marks(class_sel.get(), frame))
#             destroy_all_widgets(Frame_attendance,None)
#             return
#         elif frame == attendance_frame:
#             class_sel.bind('<<ComboboxSelected>>', lambda event: fetch_time_slot(class_sel.get()))
#
#
#         def fetch_time_slot(selected_subject):
#             destroy_all_widgets(frame,class_lbl)
#             time_slots = []
#             try:
#                 sql_time_slot = "SELECT ts.day, ts.start_time, ts.end_time FROM time_slot ts JOIN subject s ON ts.subject = s.code WHERE s.name = %s;"
#                 with connection.cursor() as cursor:
#                     cursor.execute(sql_time_slot, (selected_subject,))
#                     result_time_slot = cursor.fetchall()
#                     if result_time_slot:
#                         for slot in result_time_slot:
#                             day, start_time, end_time = slot
#                             time_slots.append(f"{day}: {start_time} - {end_time}")
#                     else:
#                         tk.messagebox.showerror("Error", "No time slot found for selected subject")
#             except Exception as e:
#                 tk.messagebox.showerror("Error", f"Database error: {str(e)}")
#
#             # Update the time slot dropdown menu
#
#             timeSlot_lbl = ttk.Label(frame, text='Time Slot : ', style='edit.TLabel', background='white',
#                                      padding=(40, 40))
#             timeSlot_lbl.grid(row=0, column=2, sticky="e")
#             timeSlot = ttk.Combobox(frame, values=time_slots, font=(font, '12'))
#             timeSlot.grid(row=0, column=3, sticky="w", padx=20, pady=20)
#             timeSlot.bind('<<ComboboxSelected>>', lambda event: fetch_students(selected_subject, frame))
#
#     except Exception as e:
#         tk.messagebox.showerror("Error", f"Database error: {str(e)}")
#         return


### GUI ###


def bind_timeslot_combobox_event(timeSlot, selected_subject, frame):
    timeSlot.bind('<<ComboboxSelected>>', lambda event: fetch_students(selected_subject, frame))

def fetch_time_slot(selected_subject, frame):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='tintots_kindergarden'
    )

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

def bind_combobox_selection_event(class_sel, frame):
    class_sel.bind('<<ComboboxSelected>>', lambda event: fetch_time_slot(class_sel.get(), frame))

def teach_subject(user, frame, assessment_frame=None, attendance_frame=None):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='tintots_kindergarden'
    )
    global class_lbl
    subjects = []
    try:
        sql = "SELECT c.name FROM subject c JOIN staff s ON c.assigned = s.id WHERE s.id = %s;"
        with connection.cursor() as cursor:
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
            class_lbl = ttk.Label(frame, text='Subject : ', style='edit.TLabel', background='white', padding=(40, 40))
            class_lbl.grid(row=0, column=0, sticky="e")
            class_sel.bind('<<ComboboxSelected>>', lambda event: record_marks(class_sel.get(), frame))
            destroy_all_widgets(Frame_attendance, None)
            return
        elif frame == attendance_frame:
            class_sel.bind('<<ComboboxSelected>>', lambda event: fetch_time_slot(class_sel.get(), frame))

    except Exception as e:
        tk.messagebox.showerror("Error", f"Database error: {str(e)}")
        return



window = tk.Tk()
window.geometry("1000x600")
window.title("Tintots Kindergarden")
window.configure(bg="#f0e5f0")

action_btn=[]
action_frame=[]

# BUTTON STYLING #
backbtn_style = ttk.Style()
backbtn_style.configure('backBtn.TButton', padding=5,
                font=(font, 12,'bold'),
                foreground='#7E467D',
                relief=tk.FLAT,
                borderwidth=0,
                borderradius=20,
                highlightthickness=0)

activebtn_style = ttk.Style()
activebtn_style.configure('activeBtn.TButton', padding=5,
                font=(font, 13,'bold'),
                foreground='#7E467D',
                relief=tk.FLAT,
                borderwidth=50,
                borderradius=30,)

inactivebtn_style = ttk.Style()
inactivebtn_style.configure('inactiveBtn.TButton', padding=5,
                font=(font, 12),
                foreground='#868686',
                relief=tk.FLAT,
                borderwidth=50,
                borderradius=30,)

action_style = ttk.Style()
action_style.configure('actionBtn.TButton', padding=5,
                font=(font, 12,'bold'),
                foreground='black',
                relief=tk.FLAT,
                borderwidth=50,
                borderradius=30,)

action_style.configure('edit.TLabel', font=(font, 12,'bold'), foreground='black',background='#F0E5F0')
action_style.configure('heading.TLabel', font=(font, 15,'bold'), foreground='#7E467D',background='white')
action_style.configure('general.TLabel', font=(font, 12), foreground='black',background='white')
action_style.configure('edit.TEntry', font=(font, 12),padding=(5, 5, 5, 5))
action_style.configure('edit.TLabelframe', font=(font, 20, "bold"), bd=3, padding=(20, 20),background='#F0E5F0', foreground='black')
action_style.configure('general.TLabelframe', font=(font, 20, "bold"), bd=3, padding=(20, 20),background='white')

action_style.configure("general.Treeview", font=(font, 10))
action_style.configure("general.Treeview.Heading", font=(font,12,'bold'))

window.bind('<Configure>', on_window_configure)

### FRAME ###
### NAVI
Frame_buttonNav = tk.Frame(window, bd=5, relief=tk.FLAT, bg="#F0E5F0")

profile_button = ttk.Button(Frame_buttonNav, text="Profile", command=profile_clicked, style='inactiveBtn.TButton',width=15)
profile_button.grid(row=0, column=0, padx=5)
action_btn.append(profile_button)

attendance_button = ttk.Button(Frame_buttonNav, text="Attendance", command=attendance_clicked, style='inactiveBtn.TButton',width=15)
attendance_button.grid(row=0, column=1, padx=5)
action_btn.append(attendance_button)

assessment_button = ttk.Button(Frame_buttonNav, text="Assessment", command=assessment_clicked, style='inactiveBtn.TButton',width=15)
assessment_button.grid(row=0, column=2, padx=5)
action_btn.append(assessment_button)

report_button = ttk.Button(Frame_buttonNav, text="Report", command=report_clicked, style='inactiveBtn.TButton',width=15)
report_button.grid(row=0, column=4, padx=5)
position=get_staff_position(user)

# if position == 'form teacher':
#     action_btn.append(report_button)
# else:
#     report_button.grid_remove()


exit_icon = Image.open("logout.png")
exit_icon = exit_icon.resize((25, 25), Image.LANCZOS)
exit_icon = ImageTk.PhotoImage(exit_icon)
exit_button = ttk.Button(Frame_buttonNav, image=exit_icon,text="Exit", command=window.quit, style='activeBtn.TButton')
exit_button.grid(row=0, column=5, sticky="e")
# Configure column weights to distribute space evenly
Frame_buttonNav.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)


### FRAME 1
Frame_profile = tk.Frame(window, bd=5, relief=tk.FLAT, bg="white")
action_frame.append(Frame_profile)
display_userPic(Frame_profile, 180, 180, user)
Editprofile_button = ttk.Button(Frame_profile, text="Edit Profile", command=lambda: edit_profile(user), style='actionBtn.TButton',width=15)
Editprofile_button.grid(row=1, column=0, padx=5,pady=5)
profile_lblframe = ttk.LabelFrame(Frame_profile, text='PROFILE' ,style='general.TLabelframe')
profile_lblframe.grid(row=0, column=1, padx=5,sticky="nsew")
Frame_profile.columnconfigure(1, weight=1)
empty_lblframe=tk.Label(profile_lblframe,padx=30,bg='white')
empty_lblframe.grid(row=0, column=2, padx=5,sticky="nsew")
row = 0
fetch_user(user,'staff')
for field, value in user_info.items():
    value=str(value)
    if field=='profile_pic' or field=='password' or field=='salary' or field=='qualification':
        pass
    else:
        if row<=5:
            ttk.Label(profile_lblframe, text=field.capitalize() + ":", style='edit.TLabel',background='white').grid(row=row, column=0,
                                                                                                 padx=10,
                                                                                                 pady=5, sticky="w")
            ttk.Label(profile_lblframe, text=value, style='edit.TLabel',font=('normal'),background='white').grid(row=row, column=1, padx=10,
                                                                              pady=5, sticky="w")
        else:
            ttk.Label(profile_lblframe, text=field.capitalize() + ":", style='edit.TLabel',background='white').grid(row=row-6, column=3,
                                                                                                 padx=10,
                                                                                                 pady=5, sticky="w")
            ttk.Label(profile_lblframe, text=value, style='edit.TLabel',font=('normal'),background='white').grid(row=row-6, column=4, padx=10,
                                                                  pady=5, sticky="w")
        row += 1

# ttk.Label(profile_lblframe, text=user_info['qualification'], style='edit.TLabel', font=('normal'), background='white').grid(row=row,
#                                                                                                            column=1,
#                                                                                                            padx=10,
#                                                                                                            pady=5,
#                                                                                                         sticky="w")
ttk.Label(Frame_profile, text="Qualification", style='edit.TLabel', background='white').grid(row=1, column=1,padx=10,
        pady=5, sticky="w")
# Create a Text widget for displaying the content
content_text = tk.Text(Frame_profile, wrap="word",font=(font,12), borderwidth=0, highlightthickness=0)
content_text.grid(row=2, column=1, sticky="nsew")

# Create a vertical scrollbar
qualification = tk.Scrollbar(Frame_profile, orient="vertical", command=content_text.yview, borderwidth=0, highlightthickness=0)
qualification.grid(row=3, column=1, sticky="nsew")
content_text.config(yscrollcommand=qualification.set)

# Insert the content text into the Text widget
content_text.insert("1.0", user_info['qualification'])
content_text.config(state="disabled")




# FRAME 2
Frame_attendance = tk.Frame(window, bd=5, relief=tk.FLAT, bg="white")
action_frame.append(Frame_attendance)
Frame_attendance.columnconfigure(1, weight=1)





# FRAME 3
Frame_assessment = tk.Frame(window, bd=5, relief=tk.FLAT, bg="white")
action_frame.append(Frame_assessment)





# FRAME 4 -Report, only available to form teacher
Frame_report = tk.Frame(window, bd=5, relief=tk.FLAT, bg="white")
action_frame.append(Frame_report)
Frame_report.columnconfigure(1, weight=1)

search_entry = ttk.Entry(Frame_report, width=30,style='edit.TEntry')
search_entry.grid(row=0, column=3, padx=10, pady=10,sticky='e')

all_student = {}
searching={}




def search_students():
    search_text = search_entry.get()

    if not search_text:
        # If search text is empty, reset the tree to show all items
        reset_student_table()
        return
    else:
        searching.clear()
        for id, name in (all_student.items()):
            if search_text.isdigit():
                if int(search_text) == id:
                    searching[id] = name
            else:
                if search_text.lower() in name.lower():
                    searching[id] = name

        if searching:
            student_tree.delete(*student_tree.get_children())
            for i, (student_id, student_name) in enumerate(searching.items(), start=1):
                student_tree.insert("", "end", values=(str(i), str(student_id), student_name))
        else:
            tk.messagebox.showinfo("No Student Found", "No student matching the search criteria was found.")


def reset_student_table():
    student_tree.delete(*student_tree.get_children())
    populate_student_table()



# Create the search button
search_button = ttk.Button(Frame_report, text="Search", style='actionBtn.TButton', command=search_students)
search_button.grid(row=0, column=4, padx=10, pady=10,sticky='w')

# Table to display student information
columns = ("No.", "Student ID", "Student Name")
student_tree = ttk.Treeview(Frame_report, columns=columns, show="headings",style="general.Treeview")
for col in columns:
    student_tree.heading(col, text=col,anchor="center")
student_tree.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky='nsew')

def view_performance_report():
    selected_item = student_tree.selection()
    if selected_item:
        values = student_tree.item(selected_item, "values")
        student_id = values[1]  # Assuming the student ID is in the second column
        display_performance_report(student_id)
    else:
        tk.messagebox.showinfo("No Student Selected from view button", "Please select a student from the table.")

def on_select(event):
    selected_item = student_tree.selection()
    if selected_item:
        values = student_tree.item(selected_item, "values")
        student_id = values[1]  # Assuming the student ID is in the second column
        display_performance_report(student_id)
    else:
        # Check if the selection is being cleared
        if event.widget.focus():
            tk.messagebox.showinfo("No Student Selected from table", "Please select a student from the table.")


# Bind the on_select function to the Treeview widget
student_tree.bind("<<TreeviewSelect>>", on_select)


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


def display_performance_report(student_id):
    view_button.configure(state='disabled')
    report_window = tk.Toplevel(window, bg='#F0E5F0',pady=20,padx=20)
    report_window.title("Performance Report")
    report_window.geometry(f"+300+80")

    fetch_user(student_id, 'stud_ms')
    row = 1
    for field, value in stud_info.items():
        value = str(value)
        if field == 'profile_pic':
            load_profilePic(report_window, 80, 80, value)
        elif field == 'annual_review' or field == 'subject' or field=='year':
            pass
        else:
            ttk.Label(report_window, text=field.capitalize() + ":", style='edit.TLabel').grid(row=row, column=0,
                                                                                              padx=10,
                                                                                              pady=5, sticky="w")
            ttk.Label(report_window, text=value, style='edit.TLabel', font=('normal')).grid(
                row=row, column=1, padx=10,
                pady=5, sticky="w")

            row += 1
    ttk.Label(report_window, text="Year: "+str(stud_info['year']), style='edit.TLabel').grid(row=0, column=4,columnspan=2, padx=20, pady=20,sticky='w')

    report_detail = ttk.LabelFrame(report_window, text='Academic Report', style='edit.TLabelframe')
    report_detail.grid(row=1, rowspan=row-1, column=4, columnspan=2, padx=20, pady=20)
    ttk.Label(report_detail, text="No.", style='edit.TLabel').grid(row=1, column=0)
    ttk.Label(report_detail, text="Subject", style='edit.TLabel').grid(row=1, column=1)
    ttk.Label(report_detail, text="Midterm", style='edit.TLabel').grid(row=1, column=2)
    ttk.Label(report_detail, text="Final Exam", style='edit.TLabel').grid(row=1, column=3)
    ttk.Label(report_detail, text="Grade", style='edit.TLabel').grid(row=1, column=4)
    ttk.Label(report_detail, text="Attendance(%)", style='edit.TLabel').grid(row=1, column=5)
    separator = ttk.Separator(report_detail, orient='horizontal')
    separator.grid(row=2, column=0, columnspan=6, sticky='ew')

    ttk.Label(report_window, text="Form Teacher Comment:", style='edit.TLabel').grid(row=row, column=4,columnspan=2, padx=20, pady=20,sticky='w')
    comment_entry = ttk.Entry(report_window, style='edit.TEntry')
    comment_entry.insert(0, stud_info['annual_review'])
    comment_entry.grid(row=row, column=5,columnspan=2, padx=20, pady=20,sticky='we')

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
        cursor.execute(sql, int(student_id,))
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
                attendance_percentage = (atten_count.count(0) / len(atten_count) * 100) if len(atten_count) != 0 else 0
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
            sql = "UPDATE stud_ms SET annual_review = %s WHERE id = %s;"
            cursor.execute(sql, (comment_entry.get(), stud_id))
            connection.commit()
            report_window.destroy()  # Close the report window
            view_button.configure(state='normal')
        except Exception as e:
            tk.messagebox.showerror("Error", f"Database error: {str(e)}")

    def download_report():
        try:
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

    done_button = ttk.Button(report_window, text="Done", style='actionBtn.TButton', command=lambda: submit_close(student_id))
    done_button.grid(row=row+1, column=4, padx=20,sticky='e')
    download_button = ttk.Button(report_window, text="Download", style='actionBtn.TButton',command=download_report)
    download_button.grid(row=row+1, column=5, padx=20,sticky='e')



view_button = ttk.Button(Frame_report, text="View", command=view_performance_report,style='activeBtn.TButton',)
view_button.grid(row=2,  column=3, padx=10, pady=10, sticky='e')




def populate_student_table():
    for i, (student_id, student_name) in enumerate(all_student.items(), start=1):
        student_tree.insert("", "end", values=(str(i), str(student_id), student_name))

def fetch_all_stud():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='tintots_kindergarden'
    )
    cursor = connection.cursor()
    try:
        sql = "SELECT id, name FROM stud_ms ;"
        cursor.execute(sql)
        students = cursor.fetchall()
        if students:
            for result in students:
                all_student[result[0]] = result[1]
        else:
            tk.messagebox.showerror("Error", "No Student Found!")
    except Exception as e:
        tk.messagebox.showerror("Error", f"Database error: {str(e)}")

fetch_all_stud()
populate_student_table()


show_frame(Frame_profile)
set_active_button(profile_button)

window.mainloop()