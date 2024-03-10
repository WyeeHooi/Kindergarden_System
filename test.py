import tkinter as tk
from tkinter import ttk

class HTMLCheckbox(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.checked = False
        self.width = 20
        self.height = 20
        self.bind("<Button-1>", self.toggle_checked)
        self.draw_checkbox()

    def toggle_checked(self, event):
        self.checked = not self.checked
        self.draw_checkbox()

    def draw_checkbox(self):
        self.delete("checkbox")
        if self.checked:
            self.create_rectangle(0, 0, self.width, self.height, fill="lightgreen", outline="black", tags="checkbox")
            self.create_line(2, 2, self.width - 2, self.height - 2, fill="black", width=2, tags="checkbox")
            self.create_line(self.width - 2, 2, 2, self.height - 2, fill="black", width=2, tags="checkbox")
        else:
            self.create_rectangle(0, 0, self.width, self.height, fill="white", outline="black", tags="checkbox")

def insert_checkbox(tree, item, column):
    checkbox = HTMLCheckbox(tree, width=20, height=20)
    tree.column(item, column=column, window=checkbox)

# Example usage:
root = tk.Tk()

tree = ttk.Treeview(root, columns=("No.", "Student ID", "Student Name", "Attendance"), show="headings")
tree.grid(row=1, columnspan=4, padx=20, pady=20, sticky="nsew")
tree.heading("No.", text="No.")
tree.heading("Student ID", text="Student ID")
tree.heading("Student Name", text="Student Name")
tree.heading("Attendance", text="Attendance")

item1 = tree.insert("", "end", values=("1", "1001", "John"))
item2 = tree.insert("", "end", values=("2", "1002", "Alice"))

insert_checkbox(tree, item1, column=3)
insert_checkbox(tree, item2, column=3)

root.mainloop()
