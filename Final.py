from tkinter import ttk, simpledialog
from tkinter import messagebox
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
import csv
import pymysql
from datetime import datetime
font = 'Lato'

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
                # show_main_interface(parent_widget, result,action_frame)  # Pass the parent widget, user details, and action frame
            else:
                messagebox.showerror("Admin Login", "Invalid username or password.")
        except pymysql.Error as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")
        finally:
            conn.close()
    else:
        messagebox.showerror("Error", "Failed to connect to database.")

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

window = tk.Tk()
screen_width = window.winfo_screenwidth() * 0.99
screen_height = window.winfo_screenheight()* 0.99
window.geometry(f"{int(screen_width)}x{int(screen_height)}+0+0")
window.title("Tintots Kindergarden")
window.configure(bg="#f0e5f0")

def login():
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

action_style.configure('edit.TEntry', font=(font, 12), padding=(5, 5, 5, 5))

action_style.configure('edit.TLabelframe', font=(font, 20, "bold"), bd=3, padding=(20, 20), background='#F0E5F0',
                       foreground='black')
action_style.configure('general.TLabelframe', font=(font, 20, "bold"), bd=3, padding=(20, 20), background='white')

action_style.configure("general.Treeview", font=(font, 10))
action_style.configure("general.Treeview.Heading", font=(font, 12, 'bold'))
####### General Settings end here ###########


window.mainloop()