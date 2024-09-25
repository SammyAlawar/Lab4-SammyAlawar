import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import sqlite3
import csv
"""School Management System Application using Tkinter and SQLite

This application provides a GUI interface for managing students, instructors, and courses in a school.
It allows users to add records, register students for courses, and view all records.

Classes:
    SchoolManagementApp: A class that creates the main application window and handles database interactions.

Functions:
    __init__(self): Initializes the application, creates the UI, and sets up the database.
    get_database_connection(self): Returns a connection to the SQLite database.
    setup_database(self): Creates the database tables if they don't exist.
    create_student_widgets(self): Creates and sets up the UI elements for adding students.
    create_instructor_widgets(self): Creates and sets up the UI elements for adding instructors.
    create_course_widgets(self): Creates and sets up the UI elements for adding courses.
    create_registration_widgets(self): Creates and sets up the UI elements for registering students to courses.
    create_view_all_widgets(self): Creates and sets up the UI elements for viewing all student records.
    add_student_record(self): Adds a new student record to the database.
    update_comboboxes(self): Updates the values in the student and course dropdown menus.
    add_instructor_record(self): Adds a new instructor record to the database.
    add_course_record(self): Adds a new course record to the database.
    register_student_course(self): Registers a student for a course.
    refresh_view_all_records(self): Refreshes the records displayed in the "View All" tab.
    clear_student_entries(self): Clears the student input fields after submission.
    clear_instructor_entries(self): Clears the instructor input fields after submission.
    clear_course_entries(self): Clears the course input fields after submission.
    on_closing(self): Handles the application close event and closes the database connection.
"""

import tkinter as tk
class SchoolManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("School Management System")
        self.geometry("600x400")
        self.database_connection = None
        self.database_cursor = None
        self.setup_database()
        
        self.tab_control = ttk.Notebook(self)
        self.tab_control.pack(expand=1, fill="both")

        self.add_student_frame = ttk.Frame(self.tab_control)
        self.add_instructor_frame = ttk.Frame(self.tab_control)
        self.add_course_frame = ttk.Frame(self.tab_control)
        self.register_course_frame = ttk.Frame(self.tab_control)
        self.view_all_frame = ttk.Frame(self.tab_control)

        self.tab_control.add(self.add_student_frame, text="Add Student")
        self.tab_control.add(self.add_instructor_frame, text="Add Instructor")
        self.tab_control.add(self.add_course_frame, text="Add Course")
        self.tab_control.add(self.register_course_frame, text="Register for Course")
        self.tab_control.add(self.view_all_frame, text="View All")

        self.create_student_widgets()
        self.create_instructor_widgets()
        self.create_course_widgets()
        self.create_registration_widgets()
        self.create_view_all_widgets()

    def get_database_connection(self):
        if not self.database_connection:
            self.database_connection = sqlite3.connect('school.db')
            self.database_cursor = self.database_connection.cursor()
        return self.database_connection

    def setup_database(self):
        conn = self.get_database_connection()
        self.database_cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                student_age INTEGER NOT NULL,
                student_email TEXT NOT NULL,
                unique_student_id TEXT NOT NULL UNIQUE
            )
        """)
        self.database_cursor.execute("""
            CREATE TABLE IF NOT EXISTS instructors (
                instructor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                instructor_name TEXT NOT NULL,
                instructor_age INTEGER NOT NULL,
                instructor_email TEXT NOT NULL,
                unique_instructor_id TEXT NOT NULL UNIQUE
            )
        """)
        self.database_cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                unique_course_id TEXT NOT NULL UNIQUE,
                course_title TEXT NOT NULL,
                course_instructor_id TEXT NOT NULL,
                FOREIGN KEY (course_instructor_id) REFERENCES instructors (unique_instructor_id)
            )
        """)
        self.database_cursor.execute("""
            CREATE TABLE IF NOT EXISTS registrations (
                registration_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_ref_id TEXT NOT NULL,
                course_ref_id TEXT NOT NULL,
                FOREIGN KEY (student_ref_id) REFERENCES students (unique_student_id),
                FOREIGN KEY (course_ref_id) REFERENCES courses (unique_course_id)
            )
        """)
        conn.commit()

    def create_student_widgets(self):
        tk.Label(self.add_student_frame, text="Name:").pack()
        self.student_name_entry = tk.Entry(self.add_student_frame)
        self.student_name_entry.pack()

        tk.Label(self.add_student_frame, text="Age:").pack()
        self.student_age_entry = tk.Entry(self.add_student_frame)
        self.student_age_entry.pack()

        tk.Label(self.add_student_frame, text="Email:").pack()
        self.student_email_entry = tk.Entry(self.add_student_frame)
        self.student_email_entry.pack()

        tk.Label(self.add_student_frame, text="Student ID:").pack()
        self.student_id_entry = tk.Entry(self.add_student_frame)
        self.student_id_entry.pack()

        tk.Button(self.add_student_frame, text="Add Student", command=self.add_student_record).pack()

    def create_instructor_widgets(self):
        tk.Label(self.add_instructor_frame, text="Name:").pack()
        self.instructor_name_entry = tk.Entry(self.add_instructor_frame)
        self.instructor_name_entry.pack()

        tk.Label(self.add_instructor_frame, text="Age:").pack()
        self.instructor_age_entry = tk.Entry(self.add_instructor_frame)
        self.instructor_age_entry.pack()

        tk.Label(self.add_instructor_frame, text="Email:").pack()
        self.instructor_email_entry = tk.Entry(self.add_instructor_frame)
        self.instructor_email_entry.pack()

        tk.Label(self.add_instructor_frame, text="Instructor ID:").pack()
        self.instructor_id_entry = tk.Entry(self.add_instructor_frame)
        self.instructor_id_entry.pack()

        tk.Button(self.add_instructor_frame, text="Add Instructor", command=self.add_instructor_record).pack()

    def create_course_widgets(self):
        tk.Label(self.add_course_frame, text="Course ID:").pack()
        self.course_id_entry = tk.Entry(self.add_course_frame)
        self.course_id_entry.pack()

        tk.Label(self.add_course_frame, text="Course Name:").pack()
        self.course_name_entry = tk.Entry(self.add_course_frame)
        self.course_name_entry.pack()

        tk.Label(self.add_course_frame, text="Instructor ID:").pack()
        self.course_instructor_id_entry = tk.Entry(self.add_course_frame)
        self.course_instructor_id_entry.pack()

        tk.Button(self.add_course_frame, text="Add Course", command=self.add_course_record).pack()

    def create_registration_widgets(self):
        tk.Label(self.register_course_frame, text="Select Student:").pack()
        self.student_combobox = ttk.Combobox(self.register_course_frame)
        self.student_combobox.pack()
        
        tk.Label(self.register_course_frame, text="Select Course:").pack()
        self.course_combobox = ttk.Combobox(self.register_course_frame)
        self.course_combobox.pack()
        self.update_comboboxes()
        tk.Button(self.register_course_frame, text="Register", command=self.register_student_course).pack()
        
    def create_view_all_widgets(self):
        self.view_all_tree = ttk.Treeview(self.view_all_frame, columns=("ID", "Name", "Age", "Email", "Additional Info"), show="headings")
        self.view_all_tree.heading("ID", text="ID")
        self.view_all_tree.heading("Name", text="Name")
        self.view_all_tree.heading("Age", text="Age")
        self.view_all_tree.heading("Email", text="Email")
        self.view_all_tree.heading("Additional Info", text="Additional Info")
        self.view_all_tree.pack(expand=1, fill="both")

        tk.Button(self.view_all_frame, text="Refresh", command=self.refresh_view_all_records).pack()
     
    def add_student_record(self):
        name = self.student_name_entry.get()
        age = int(self.student_age_entry.get())
        email = self.student_email_entry.get()
        unique_id = self.student_id_entry.get()
        
        try:
            conn = self.get_database_connection()
            self.database_cursor.execute(""" 
                INSERT INTO students (student_name, student_age, student_email, unique_student_id)
                VALUES (?, ?, ?, ?)
            """, (name, age, email, unique_id))
            conn.commit()
            messagebox.showinfo("Success", "Student added successfully")
            self.clear_student_entries()
            
            # Update the dropdowns after adding a student
            self.update_comboboxes()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding student: {e}")

    def update_comboboxes(self):
        self.student_combobox['values'] = [row[0] for row in self.database_cursor.execute("SELECT student_name FROM students").fetchall()]
        self.course_combobox['values'] = [row[0] for row in self.database_cursor.execute("SELECT course_title FROM courses").fetchall()]

    def add_instructor_record(self):
        name = self.instructor_name_entry.get()
        age = int(self.instructor_age_entry.get())
        email = self.instructor_email_entry.get()
        unique_id = self.instructor_id_entry.get()
        
        try:
            conn = self.get_database_connection()
            self.database_cursor.execute(""" 
                INSERT INTO instructors (instructor_name, instructor_age, instructor_email, unique_instructor_id)
                VALUES (?, ?, ?, ?)
            """, (name, age, email, unique_id))
            conn.commit()
            messagebox.showinfo("Success", "Instructor added successfully")
            self.clear_instructor_entries()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding instructor: {e}")

    def add_course_record(self):
        unique_id = self.course_id_entry.get()
        title = self.course_name_entry.get()
        instructor_id = self.course_instructor_id_entry.get()
        
        try:
            conn = self.get_database_connection()
            self.database_cursor.execute(""" 
                INSERT INTO courses (unique_course_id, course_title, course_instructor_id)
                VALUES (?, ?, ?)
            """, (unique_id, title, instructor_id))
            conn.commit()
            messagebox.showinfo("Success", "Course added successfully")
            self.clear_course_entries()
            self.update_comboboxes()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding course: {e}")

    def register_student_course(self):
        selected_student_name = self.student_combobox.get()
        selected_course_name = self.course_combobox.get()
        
        try:
            conn = self.get_database_connection()
            self.database_cursor.execute("SELECT unique_student_id FROM students WHERE student_name = ?", (selected_student_name,))
            student_ref_id = self.database_cursor.fetchone()[0]
            self.database_cursor.execute("SELECT unique_course_id FROM courses WHERE course_title = ?", (selected_course_name,))
            course_ref_id = self.database_cursor.fetchone()[0]
            self.database_cursor.execute(""" 
                INSERT INTO registrations (student_ref_id, course_ref_id)
                VALUES (?, ?)
            """, (student_ref_id, course_ref_id))
            conn.commit()
            messagebox.showinfo("Success", "Student registered for course successfully")
            self.update_comboboxes()
        except Exception as e:
            messagebox.showerror("Error", f"Error registering student for course: {e}")

    def refresh_view_all_records(self):
        for i in self.view_all_tree.get_children():
            self.view_all_tree.delete(i)
        records = self.database_cursor.execute("SELECT * FROM students").fetchall()
        for record in records:
            self.view_all_tree.insert("", "end", values=record)

    def clear_student_entries(self):
        self.student_name_entry.delete(0, tk.END)
        self.student_age_entry.delete(0, tk.END)
        self.student_email_entry.delete(0, tk.END)
        self.student_id_entry.delete(0, tk.END)

    def clear_instructor_entries(self):
        self.instructor_name_entry.delete(0, tk.END)
        self.instructor_age_entry.delete(0, tk.END)
        self.instructor_email_entry.delete(0, tk.END)
        self.instructor_id_entry.delete(0, tk.END)

    def clear_course_entries(self):
        self.course_id_entry.delete(0, tk.END)
        self.course_name_entry.delete(0, tk.END)
        self.course_instructor_id_entry.delete(0, tk.END)

    def on_closing(self):
        if self.database_connection:
            self.database_connection.close()
        self.destroy()

if __name__ == "__main__":
    app = SchoolManagementApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
