import tkinter as tk
from tkinter import ttk

def on_edit(event):
    item = tree.focus()
    column = tree.identify_column(event.x)
    if column == '#1':  # Check if the clicked column is the second one (index starts from 1)
        entry.delete(0, 'end')
        entry.insert(0, tree.item(item)['values'][0])
        entry.place(relx=0.5, rely=0.5, anchor='center')
        entry.focus_set()
        entry.bind('<Return>', lambda event: end_edit(item))

def end_edit(item):
    value = entry.get()
    tree.item(item, values=(value,))
    entry.place_forget()

root = tk.Tk()

tree = ttk.Treeview(root)
tree['columns'] = ('value',)
tree.heading('#0', text='ID')
tree.heading('value', text='Value')

# Insert some sample data
for i in range(5):
    tree.insert('', 'end', text=str(i), values=('Value ' + str(i)))

tree.pack()

# Entry widget for editing
entry = tk.Entry(root, justify='center')

tree.bind('<Double-1>', on_edit)

root.mainloop()
