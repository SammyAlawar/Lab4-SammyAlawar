import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QTabWidget, QComboBox, QMessageBox, QFileDialog, QFormLayout
)
from PyQt5.QtCore import Qt
import sqlite3
import csv

"""
School Management System
------------------------
This PyQt5-based GUI application manages students, instructors, and courses, 
allowing users to add, view, and register students for courses. The data is stored in an SQLite database.

Classes and Methods:
--------------------
SchoolManagementSystem(QMainWindow):
    - __init__(self): Initializes the GUI, sets up database connection, and creates tabs for different functionalities.
    - initialize_database(self): Sets up the SQLite database and creates tables for students, instructors, courses, and registrations.
    - create_add_student_widgets(self): Creates input fields and buttons for adding a student to the database.
    - create_add_instructor_widgets(self): Creates input fields and buttons for adding an instructor to the database.
    - create_add_course_widgets(self): Creates input fields and buttons for adding a course to the database.
    - create_register_course_widgets(self): Creates dropdowns and buttons for registering a student for a course.
    - create_view_all_widgets(self): Sets up a table to display students and an option to export data to CSV.
    - refresh_dropdowns(self): Updates the student and course dropdowns when new data is added.
    - add_student(self): Adds a new student to the 'students' table in the database.
    - add_instructor(self): Adds a new instructor to the 'instructors' table in the database.
    - add_course(self): Adds a new course to the 'courses' table in the database.
    - register_course(self): Registers a student for a course and stores this information in the 'registrations' table.
    - refresh_view_all(self): Displays all students in the table on the 'View All' tab.
    - export_to_csv(self): Exports the data from the 'View All' table into a CSV file.
    - clear_student_inputs(self): Clears the input fields for adding a student.
    - clear_instructor_inputs(self): Clears the input fields for adding an instructor.
    - clear_course_inputs(self): Clears the input fields for adding a course.

    Database Tables:
    ----------------
    - students: Stores student information (id, name, age, email, unique_id).
    - instructors: Stores instructor information (id, name, age, email, unique_id).
    - courses: Stores course information (id, course_id, course_name, instructor_id).
    - registrations: Stores course registrations (student_id, course_id).
"""
class SchoolManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 800, 600)
        self.db_connection = None
        self.cursor = None
        self.initialize_database()
        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        self.add_student_tab = QWidget()
        self.add_instructor_tab = QWidget()
        self.add_course_tab = QWidget()
        self.register_course_tab = QWidget()
        self.view_all_tab = QWidget()
        
        self.tabs.addTab(self.add_student_tab, "Add Student")
        self.tabs.addTab(self.add_instructor_tab, "Add Instructor")
        self.tabs.addTab(self.add_course_tab, "Add Course")
        self.tabs.addTab(self.register_course_tab, "Register for Course")
        self.tabs.addTab(self.view_all_tab, "View All")
        
        self.create_add_student_widgets()
        self.create_add_instructor_widgets()
        self.create_add_course_widgets()
        self.create_register_course_widgets()
        self.create_view_all_widgets()

    def initialize_database(self):
        self.db_connection = sqlite3.connect("school_management.db")
        self.cursor = self.db_connection.cursor()
        # Create tables if they do not exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                email TEXT NOT NULL,
                unique_id TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS instructors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                email TEXT NOT NULL,
                unique_id TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id TEXT NOT NULL,
                course_name TEXT NOT NULL,
                instructor_id TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS registrations (
                student_id INTEGER,
                course_id INTEGER,
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (course_id) REFERENCES courses(id)
            )
        """)

        self.db_connection.commit()

    def create_add_student_widgets(self):
        layout = QFormLayout()
        self.student_name = QLineEdit()
        self.student_age = QLineEdit()
        self.student_email = QLineEdit()
        self.student_id = QLineEdit()
        layout.addRow(QLabel("Name:"), self.student_name)
        layout.addRow(QLabel("Age:"), self.student_age)
        layout.addRow(QLabel("Email:"), self.student_email)
        layout.addRow(QLabel("Student ID:"), self.student_id)
        
        add_button = QPushButton("Add Student")
        add_button.clicked.connect(self.add_student)
        layout.addWidget(add_button)
        self.add_student_tab.setLayout(layout)

    def create_add_instructor_widgets(self):
        layout = QFormLayout()
        self.instructor_name = QLineEdit()
        self.instructor_age = QLineEdit()
        self.instructor_email = QLineEdit()
        self.instructor_id = QLineEdit()
        layout.addRow(QLabel("Name:"), self.instructor_name)
        layout.addRow(QLabel("Age:"), self.instructor_age)
        layout.addRow(QLabel("Email:"), self.instructor_email)
        layout.addRow(QLabel("Instructor ID:"), self.instructor_id)
        
        add_button = QPushButton("Add Instructor")
        add_button.clicked.connect(self.add_instructor)
        layout.addWidget(add_button)
        self.add_instructor_tab.setLayout(layout)

    def create_add_course_widgets(self):
        layout = QFormLayout()
        self.course_id = QLineEdit()
        self.course_name = QLineEdit()
        self.instructor_id_course = QLineEdit()
        layout.addRow(QLabel("Course ID:"), self.course_id)
        layout.addRow(QLabel("Course Name:"), self.course_name)
        layout.addRow(QLabel("Instructor ID:"), self.instructor_id_course)
        
        add_button = QPushButton("Add Course")
        add_button.clicked.connect(self.add_course)
        layout.addWidget(add_button)
        self.add_course_tab.setLayout(layout)

    def create_register_course_widgets(self):
        layout = QFormLayout()
        self.student_dropdown = QComboBox()
        self.course_dropdown = QComboBox()
        layout.addRow(QLabel("Select Student:"), self.student_dropdown)
        layout.addRow(QLabel("Select Course:"), self.course_dropdown)
        
        register_button = QPushButton("Register")
        register_button.clicked.connect(self.register_course)
        layout.addWidget(register_button)
        self.register_course_tab.setLayout(layout)
        
        self.refresh_dropdowns()

    def create_view_all_widgets(self):
        self.view_all_table = QTableWidget()
        self.view_all_table.setColumnCount(5)
        self.view_all_table.setHorizontalHeaderLabels(['ID', 'Name', 'Age', 'Email', 'Additional Info'])
        self.view_all_table.horizontalHeader().setStretchLastSection(True)
        
        layout = QVBoxLayout()
        layout.addWidget(self.view_all_table)
        
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_view_all)
        layout.addWidget(refresh_button)
        
        export_button = QPushButton("Export to CSV")
        export_button.clicked.connect(self.export_to_csv)
        layout.addWidget(export_button)
        
        self.view_all_tab.setLayout(layout)

    def refresh_dropdowns(self):
        self.student_dropdown.clear()
        self.course_dropdown.clear()
        
        self.cursor.execute("SELECT name FROM students")
        students = [row[0] for row in self.cursor.fetchall()]
        self.student_dropdown.addItems(students)
        
        self.cursor.execute("SELECT course_name FROM courses")
        courses = [row[0] for row in self.cursor.fetchall()]
        self.course_dropdown.addItems(courses)

    def add_student(self):
        name = self.student_name.text()
        age = int(self.student_age.text())
        email = self.student_email.text()
        student_id = self.student_id.text()
        
        try:
            self.cursor.execute("""
                INSERT INTO students (name, age, email, unique_id) 
                VALUES (?, ?, ?, ?)
            """, (name, age, email, student_id))
            self.db_connection.commit()
            QMessageBox.information(self, "Success", "Student added successfully")
            self.clear_student_inputs()
            self.refresh_dropdowns()  # Refresh dropdowns after adding a student
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error adding student: {e}")

    def add_instructor(self):
        name = self.instructor_name.text()
        age = int(self.instructor_age.text())
        email = self.instructor_email.text()
        instructor_id = self.instructor_id.text()
        
        try:
            self.cursor.execute("""
                INSERT INTO instructors (name, age, email, unique_id) 
                VALUES (?, ?, ?, ?)
            """, (name, age, email, instructor_id))
            self.db_connection.commit()
            QMessageBox.information(self, "Success", "Instructor added successfully")
            self.clear_instructor_inputs()
            self.refresh_dropdowns()  # Refresh dropdowns if necessary
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error adding instructor: {e}")

    def add_course(self):
        course_id = self.course_id.text()
        course_name = self.course_name.text()
        instructor_id = self.instructor_id_course.text()
        
        try:
            self.cursor.execute("""
                INSERT INTO courses (course_id, course_name, instructor_id) 
                VALUES (?, ?, ?)
            """, (course_id, course_name, instructor_id))
            self.db_connection.commit()
            QMessageBox.information(self, "Success", "Course added successfully")
            self.clear_course_inputs()
            self.refresh_dropdowns()  # Refresh dropdowns after adding a course
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error adding course: {e}")

    def register_course(self):
        student_name = self.student_dropdown.currentText()
        course_name = self.course_dropdown.currentText()
        
        try:
            # Get the student ID from the student's name
            self.cursor.execute("SELECT id FROM students WHERE name = ?", (student_name,))
            student_id = self.cursor.fetchone()[0]
            
            # Get the course ID from the course name
            self.cursor.execute("SELECT id FROM courses WHERE course_name = ?", (course_name,))
            course_id = self.cursor.fetchone()[0]
            
            # Insert into the registrations table
            self.cursor.execute("""
                INSERT INTO registrations (student_id, course_id)
                VALUES (?, ?)
            """, (student_id, course_id))
            self.db_connection.commit()
            QMessageBox.information(self, "Success", "Course registered successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error registering course: {e}")

      
           

    def refresh_view_all(self):
        # Clear the table
        self.view_all_table.clearContents()
        self.view_all_table.setRowCount(0)

        # Fetch and display students
        self.cursor.execute("SELECT id, name, age, email, unique_id FROM students")
        students = self.cursor.fetchall()
        for row_data in students:
            row_position = self.view_all_table.rowCount()
            self.view_all_table.insertRow(row_position)
            for column, data in enumerate(row_data):
                self.view_all_table.setItem(row_position, column, QTableWidgetItem(str(data)))

        # Adjust column count and header for the instructors and courses if needed


    def export_to_csv(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv);;All Files (*)")
        if filename:
            try:
                with open(filename, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["ID", "Name", "Age", "Email", "Additional Info"])
                    for row in range(self.view_all_table.rowCount()):
                        row_data = [self.view_all_table.item(row, col).text() for col in range(self.view_all_table.columnCount())]
                        writer.writerow(row_data)
                QMessageBox.information(self, "Success", "Data exported successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error exporting data: {e}")

    def clear_student_inputs(self):
        self.student_name.clear()
        self.student_age.clear()
        self.student_email.clear()
        self.student_id.clear()

    def clear_instructor_inputs(self):
        self.instructor_name.clear()
        self.instructor_age.clear()
        self.instructor_email.clear()
        self.instructor_id.clear()

    def clear_course_inputs(self):
        self.course_id.clear()
        self.course_name.clear()
        self.instructor_id_course.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SchoolManagementSystem()
    window.show()
    sys.exit(app.exec_())
