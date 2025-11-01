# Import libraries
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import re

# Database setup
def create_db():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            uid INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            contact TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL,
            course TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Validation functions
def validate_contact(contact):
    return re.match(r'^\d{10}$', contact) is not None

def validate_email(email):
    return '@' in email

def validate_age(age):
    try:
        age_int = int(age)
        return 10 <= age_int <= 100
    except ValueError:
        return False

def validate_name_course(value):
    return len(value.strip()) > 0

def validate_uid(uid):
    try:
        int(uid)
        return True
    except ValueError:
        return False

# CRUD Functions
def add_student():
    uid = uid_entry.get().strip()
    name = name_entry.get().strip()
    contact = contact_entry.get().strip()
    email = email_entry.get().strip()
    age = age_entry.get().strip()
    course = course_entry.get().strip()
    
    if not (validate_uid(uid) and validate_name_course(name) and validate_contact(contact) and validate_email(email) and validate_age(age) and validate_name_course(course)):
        messagebox.showerror("Error", "Invalid input! Check fields: UID must be integer, Name/Course not empty, Contact=10 digits, Email has '@', Age=10-100.")
        return
    
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO students (uid, name, contact, email, age, course) VALUES (?, ?, ?, ?, ?, ?)',
                       (int(uid), name, contact, email, int(age), course))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully!")
        clear_fields()
        view_students()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "UID already exists. Choose a unique UID.")
    conn.close()

def update_student():
    uid = uid_entry.get().strip()
    if not validate_uid(uid):
        messagebox.showerror("Error", "Enter a valid integer UID to update.")
        return
    
    name = name_entry.get().strip()
    contact = contact_entry.get().strip()
    email = email_entry.get().strip()
    age = age_entry.get().strip()
    course = course_entry.get().strip()
    
    if not (validate_name_course(name) and validate_contact(contact) and validate_email(email) and validate_age(age) and validate_name_course(course)):
        messagebox.showerror("Error", "Invalid input! Check fields.")
        return
    
    # Open DB connection
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    
    # Perform the update query
    cursor.execute('UPDATE students SET name=?, contact=?, email=?, age=?, course=? WHERE uid=?',
                   (name, contact, email, int(age), course, int(uid)))
    
    if cursor.rowcount == 0:
        messagebox.showerror("Error", "Student with this UID not found.")
    else:
        messagebox.showinfo("Success", "Student updated successfully!")
        clear_fields()
        view_students()  # Refresh the view after updating

    conn.commit()
    conn.close()

def delete_student():
    uid = uid_entry.get().strip()
    if not validate_uid(uid):
        messagebox.showerror("Error", "Enter a valid integer UID to delete.")
        return
    
    # Open DB connection
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    
    # Perform the delete query
    cursor.execute('DELETE FROM students WHERE uid=?', (int(uid),))
    
    if cursor.rowcount == 0:
        messagebox.showerror("Error", "Student with this UID not found.")
    else:
        messagebox.showinfo("Success", "Student deleted successfully!")
        clear_fields()
        view_students()  # Refresh the view after deletion

    conn.commit()
    conn.close()

def search_student():
    uid = search_uid_entry.get().strip()
    if not validate_uid(uid):
        messagebox.showerror("Error", "Enter a valid integer UID to search.")
        return
    
    for row in tree.get_children():
        tree.delete(row)
    
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students WHERE uid=?', (int(uid),))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        # Capitalize name and convert course to uppercase
        name = ' '.join([word.capitalize() for word in row[1].split()])
        course = row[5].upper()
        tree.insert('', tk.END, values=(row[0], name, row[2], row[3], row[4], course))
    else:
        messagebox.showerror("Error", "Student not found.")
        view_students()  # Revert to showing all students if not found

def view_students():
    for row in tree.get_children():
        tree.delete(row)
    
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    rows = cursor.fetchall()
    conn.close()
    
    for row in rows:
        # Capitalize name and uppercase course
        name = ' '.join([word.capitalize() for word in row[1].split()])
        course = row[5].upper()
        tree.insert('', tk.END, values=(row[0], name, row[2], row[3], row[4], course))

def clear_fields():
    uid_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)

# GUI Setup
create_db()
root = tk.Tk()
root.title("Student Management System")
root.geometry("900x600")
root.configure(bg="#f0f0f0")

# Style
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Arial", 10), padding=5)
style.configure("TLabel", font=("Arial", 10), background="#f0f0f0")
style.configure("TEntry", font=("Arial", 10))

# Frames
form_frame = ttk.Frame(root, padding=10)
form_frame.pack(side=tk.TOP, fill=tk.X)

table_frame = ttk.Frame(root, padding=10)
table_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# Form Labels and Entries
ttk.Label(form_frame, text="UID (Integer, Unique):").grid(row=0, column=0, sticky=tk.W, pady=5)
uid_entry = ttk.Entry(form_frame)
uid_entry.grid(row=0, column=1, pady=5, padx=5)

ttk.Label(form_frame, text="Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
name_entry = ttk.Entry(form_frame)
name_entry.grid(row=1, column=1, pady=5, padx=5)

ttk.Label(form_frame, text="Contact (10 digits):").grid(row=2, column=0, sticky=tk.W, pady=5)
contact_entry = ttk.Entry(form_frame)
contact_entry.grid(row=2, column=1, pady=5, padx=5)

ttk.Label(form_frame, text="Email:").grid(row=3, column=0, sticky=tk.W, pady=5)
email_entry = ttk.Entry(form_frame)
email_entry.grid(row=3, column=1, pady=5, padx=5)

ttk.Label(form_frame, text="Age:").grid(row=4, column=0, sticky=tk.W, pady=5)
age_entry = ttk.Entry(form_frame)
age_entry.grid(row=4, column=1, pady=5, padx=5)

ttk.Label(form_frame, text="Course:").grid(row=5, column=0, sticky=tk.W, pady=5)
course_entry = ttk.Entry(form_frame)
course_entry.grid(row=5, column=1, pady=5, padx=5)

# Buttons
button_frame = ttk.Frame(form_frame)
button_frame.grid(row=6, column=0, columnspan=2, pady=10)

ttk.Button(button_frame, text="Add Student", command=add_student).grid(row=0, column=0, padx=5)
ttk.Button(button_frame, text="Update Student", command=update_student).grid(row=0, column=1, padx=5)
ttk.Button(button_frame, text="Delete Student", command=delete_student).grid(row=0, column=2, padx=5)
ttk.Button(button_frame, text="Clear Fields", command=clear_fields).grid(row=0, column=3, padx=5)

# Search in Viewing Section
search_frame = ttk.Frame(table_frame)
search_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

ttk.Label(search_frame, text="Search UID:").pack(side=tk.LEFT, padx=5)
search_uid_entry = ttk.Entry(search_frame, width=20)
search_uid_entry.pack(side=tk.LEFT, padx=5)
ttk.Button(search_frame, text="Search", command=search_student).pack(side=tk.LEFT, padx=5)
ttk.Button(search_frame, text="View All", command=view_students).pack(side=tk.LEFT, padx=5)

# Table
columns = ("UID", "Name", "Contact", "Email", "Age", "Course")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.pack(fill=tk.BOTH, expand=True)

# Scrollbar
scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Initial load
view_students()
root.mainloop()