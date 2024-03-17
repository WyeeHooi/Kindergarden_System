from tkinter import ttk
import tkinter as tk

# Define your styles and other settings here
font='Lato'

window = tk.Tk()
screen_width = window.winfo_screenwidth() * 0.99
screen_height = window.winfo_screenheight() * 0.99
window.geometry(f"{int(screen_width)}x{int(screen_height)}+0+0")
window.title("Tintots Kindergarden")
window.configure(bg="#f0e5f0")

def login():
    login_frame = tk.Frame(window, background="white")
    login_frame.pack(expand=True)

    title_lbl = ttk.Label(login_frame, text="Tintots Kindergarden", font=(font, 20, 'bold'), style='heading.TLabel')
    title_lbl.grid(row=0, columnspan=2, padx=50, pady=50)

    # Create username and password labels and entry widgets
    username_label = ttk.Label(login_frame, text="Username:", style="general.TLabel")
    username_label.grid(row=1, column=0, padx=10, pady=10)
    username_entry = ttk.Entry(login_frame, width=40, style="edit.TEntry")
    username_entry.grid(row=1, column=1, padx=10, pady=10)

    password_label = ttk.Label(login_frame, text="Password:", style="general.TLabel")
    password_label.grid(row=2, column=0, padx=10, pady=10)
    password_entry = ttk.Entry(login_frame, show="*", width=40, style='edit.TEntry')
    password_entry.grid(row=2, column=1, padx=10, pady=10)

    # Admin login button
    admin_button = ttk.Button(login_frame, text="Admin", style="actionBtn.TButton")
    admin_button.grid(row=3, column=0)

    # Teacher login button
    staff_button = ttk.Button(login_frame, text="Staff",  style="actionBtn.TButton")
    staff_button.grid(row=3, column=1)

if __name__ == "__main__":
    login()
## General Setting ##
font = 'Lato'
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
