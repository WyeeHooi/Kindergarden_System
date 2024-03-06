import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import pymysql
from tkinter import PhotoImage
from PIL import Image, ImageTk
import os

font='Lato'

subjects=["Bahasa Melayu","English","Mathematics","Science","Living Skills","Physical Education","Art","Music"]

user_info={}

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

# def toggle_button_state():
#     if button.cget("state") == "normal":
#         button.config(state="disabled")
#     else:
#         button.config(state="normal")

def on_window_configure(event):
    Frame_buttonNav.place(x=0, y=0, width=window.winfo_width(), height=window.winfo_height()*0.1)
    for frame in action_frame:
        frame.place(x=0, y=window.winfo_height() * 0.1, width=window.winfo_width(),
                            height=window.winfo_height() * 0.9)


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

def assessment_clicked():
    show_frame(Frame_assessment)
    set_active_button(assessment_button)

def report_clicked():
    show_frame(Frame_report)
    set_active_button(report_button)

# Function to display the image in the frame
def display_userPic(frame, width, height, user):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT profile_pic FROM staff WHERE name=%s;"
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

def fetch_user(user):
    global user_info
    user_info = {}
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='tintots_kindergarden'
    )
    try:
        sql = "SELECT * FROM staff WHERE name=%s;"
        with connection.cursor() as cursor:
            cursor.execute(sql, (user,))
            result = cursor.fetchone()
            if result:
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
            else:
                tk.messagebox.showerror("Error", "User not found in the database")
                return
    except Exception as e:
        tk.messagebox.showerror("Error", f"Database error: {str(e)}")
        return

def edit_profile(user):
    # global user_info
    # user_info= {}
    # connection = pymysql.connect(
    #     host='localhost',
    #     user='root',
    #     password='',
    #     database='tintots_kindergarden'
    # )
    # try:
    #     sql = "SELECT * FROM staff WHERE name=%s;"
    #     with connection.cursor() as cursor:
    #         cursor.execute(sql, (user,))
    #         result = cursor.fetchone()
    #         if result:
    #             user_info['id'] = result[0]
    #             user_info['name'] = result[1]
    #             user_info['password'] = result[3]
    #             user_info['contact'] = result[2]
    #             user_info['email'] = result[6]
    #             user_info['address'] = result[5]
    #         else:
    #             tk.messagebox.showerror("Error", "User not found in the database")
    #             return
    # except Exception as e:
    #     tk.messagebox.showerror("Error", f"Database error: {str(e)}")
    #     return
    fetch_user(user)
    # Create a pop-up window for editing
    edit_window = tk.Toplevel(Frame_profile,bg='#F0E5F0')
    edit_window.title("Edit Profile")
    edit_window.geometry(f"+300+150")
    edit_detail = ttk.LabelFrame(edit_window, text=user, style='edit.TLabelframe')
    edit_detail.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Entry widgets to display and edit user info
    entries = {}
    row = 0
    for field, value in user_info.items():
        if field in ["id" , "name" , "password" , "email" , "contact"]:
            ttk.Label(edit_detail, text=field.capitalize() + ":", style='edit.TLabel').grid(row=row, column=0, padx=5,
                                                                                            pady=10, sticky="w")
            entry = ttk.Entry(edit_detail, style='edit.TEntry')
            entry.insert(0, value)
            entry.grid(row=row, column=1, padx=10, pady=10, sticky="w")
            entries[field] = entry
            if field == "id":
                entry.config(state="readonly")

            row += 1


    def save_changes():
        # Function to save the changes made by the user
        new_name = entries['name'].get()
        new_password = entries['password'].get()
        new_email = entries['email'].get()
        new_contact = entries['contact'].get()
        new_address = entries['address'].get()
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE staff SET name=%s, email=%s,password=%s,contact=%s,address=%s WHERE id=%s;"
                cursor.execute(sql, (new_name, new_email, new_password,new_contact,new_contact,user_info['id']))
                connection.commit()
                edit_window.destroy()
                tk.messagebox.showinfo("Success", "Profile updated successfully")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Database error: {str(e)}")


    # Button to save changes
    save_button = ttk.Button(edit_detail, text="Save Changes", command=save_changes, style='actionBtn.TButton')
    save_button.grid(row=row, column=0, columnspan=2, padx=5, pady=10)




### GUI ###
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
action_style.configure('edit.TEntry', font=(font, 12),padding=(5, 5, 5, 5))
action_style.configure('edit.TLabelframe', font=(font, 20, "bold"), bd=3, padding=(20, 20),background='#F0E5F0')
action_style.configure('general.TLabelframe', font=(font, 20, "bold"), bd=3, padding=(20, 20),background='white')

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
action_btn.append(report_button)

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
display_userPic(Frame_profile, 180, 180, 'hooi yee')
Editprofile_button = ttk.Button(Frame_profile, text="Edit Profile", command=lambda: edit_profile('hooi yee'), style='actionBtn.TButton',width=15)
Editprofile_button.grid(row=1, column=0, padx=5,pady=5)
profile_lblframe = ttk.LabelFrame(Frame_profile, text='PROFILE' ,style='general.TLabelframe')
profile_lblframe.grid(row=0, column=1, padx=5,sticky="nsew")
Frame_profile.columnconfigure(1, weight=1)
empty_lblframe=tk.Label(profile_lblframe,padx=30,bg='white')
empty_lblframe.grid(row=0, column=2, padx=5,sticky="nsew")
row = 0
fetch_user('hooi yee')
for field, value in user_info.items():
    value=str(value)
    if field=='profile_pic':
        pass
    else:
        if row<=6:
            ttk.Label(profile_lblframe, text=field.capitalize() + ":", style='edit.TLabel',background='white').grid(row=row, column=0,
                                                                                                 padx=10,
                                                                                                 pady=5, sticky="w")
            ttk.Label(profile_lblframe, text=value, style='edit.TLabel',font=('normal'),background='white').grid(row=row, column=1, padx=10,
                                                                              pady=5, sticky="w")
        else:
            ttk.Label(profile_lblframe, text=field.capitalize() + ":", style='edit.TLabel',background='white').grid(row=row-7, column=3,
                                                                                                 padx=10,
                                                                                                 pady=5, sticky="w")
            ttk.Label(profile_lblframe, text=value, style='edit.TLabel',font=('normal'),background='white').grid(row=row-7, column=4, padx=10,
                                                                              pady=5, sticky="w")

    row += 1



# FRAME 2
Frame_attendance = tk.Frame(window, bd=5, relief=tk.FLAT, bg="white")
action_frame.append(Frame_attendance)
class_lbl=ttk.Label(Frame_attendance,text='Class : ',style='edit.TLabel',background='white',padding=(40,40)).grid(row=0,column=0,sticky="e")
class_sel=ttk.Combobox(Frame_attendance,values=subjects,font=(font,'12')).grid(row=0,column=1,sticky="w",padx=20,pady=20)
Frame_attendance.columnconfigure(1, weight=1)

tree = ttk.Treeview(Frame_attendance, columns=("Name", "Roll Number", "Grade"), show="headings")
tree.heading("Name", text="Name")
tree.heading("Roll Number", text="Roll Number")
tree.heading("Grade", text="Grade")
tree.grid(row=1, columnspan=2, padx=20, pady=20,sticky="nsew")

# FRAME 3
Frame_assessment = tk.Frame(window, bd=5, relief=tk.FLAT, bg="red")
action_frame.append(Frame_assessment)
# FRAME 4
Frame_report = tk.Frame(window, bd=5, relief=tk.FLAT, bg="white")
action_frame.append(Frame_report)

show_frame(Frame_profile)
set_active_button(profile_button)

window.mainloop()