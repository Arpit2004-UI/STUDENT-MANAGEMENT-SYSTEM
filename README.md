*****************STUDENT MANAGEMENT SYSTEM*******
A simple desktop application using Python’s Tkinter for the GUI and SQLite for the backend database. This program allows you to add, view, update, delete, and search student records with data validation and a clean user interface.

Features
Add Student: Add new students with a unique UID and validated fields (contact, email, age).

Update Student: Modify details for existing student records using UID.

Delete Student: Remove a student from the database using the UID.

Search Student: Find students by UID and display them in the table.

View All: List all student records in a scrollable table.

Form Validation: Ensures UID is integer and unique, contact is 10 digits, email contains '@', age is 10-100, name and course fields are not empty.

Clear Fields: Easily reset the input form for new entries.

Technologies Used
Python: Programming language

Tkinter: GUI framework for the form and table

tkinter.ttk: For styled widgets (buttons, entries, table)

SQLite3: Built-in database for storing student records (students.db)

re: Regular expressions for input validation

How to Run
Make sure you have Python 3.x installed.

Save the script (e.g., main.py).

Run the script:

bash
python main.py
The application window will open.

Database
The database file students.db is created automatically (if not present) in the project directory.

The table includes columns: UID, Name, Contact, Email, Age, Course.

All records are displayed in a table with scroll support.

Screenshots
(Insert relevant screenshots here of the form and table views for illustration.)

Validation Rules
UID: Integer, unique

Name: Not empty

Contact: Exactly 10 digits

Email: Must contain @

Age: Integer between 10 and 100

Course: Not empty

Additional Notes
All operations (CRUD) are reflected immediately in the database.

Error messages and feedback are shown using message boxes for better user experience.

The program is fully local/offline; no internet or server required.

License
This project is open-source and free to use for educational purposes.
STUDENT MANAGEMENT SYSTEM
