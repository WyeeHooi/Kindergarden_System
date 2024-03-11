import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()

# Get the available themes
themes = ttk.Style().theme_names()
print(themes)

# Run the application
root.mainloop()