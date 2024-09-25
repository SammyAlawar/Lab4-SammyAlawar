import json
import re
def validate_email(email):
    """
    Validates the given email address against a regular expression pattern.
    
    The pattern checks for:
    - A local part (before the '@') that can contain letters, digits, dots, underscores, or hyphens.
    - An '@' symbol separating the local part and the domain part.
    - A domain name (after the '@') that can contain letters, digits, or hyphens.
    - A literal dot ('.') followed by a domain extension that can contain letters, digits, hyphens, or dots.

    Args:
        email (str): The email address to validate.

    Returns:
        Match object or None: If the email matches the pattern, a match object is returned;
        otherwise, None is returned.
    """
    pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(pattern, email):
        raise ValueError("Invalid Email Address")
    
    return email


def validate_name(name):
    """
    Validates the given name.

    Args:
        name (str): The name to validate.

    Returns:
        str: The valid name.

    Raises:
        ValueError: If the name is not a non-empty string.
    """
    if not isinstance(name, str) or not name:
        raise ValueError("Name must be a non-empty string.")
    return name


def validate_age(age):
    """
    Validates the given age.

    Args:
        age (int): The age to validate.

    Returns:
        int: The valid age.

    Raises:
        ValueError: If the age is not a non-negative integer.
    """
    if not isinstance(age, int) or age < 0:
        raise ValueError("Age must be a non-negative integer.")
    
    return age


def validate_studentID(id):
    """
    Validates the given student id.

    Args:
        id (string): The id to validate.

    Returns:
        string: The valid id.

    Raises:
        ValueError: If the id is not a 9 digit integer.
    """
    pattern = r'^\d{9}$'  # Regex pattern for 9-digit integers
    if not re.match(pattern, id):
        raise ValueError("Student ID must be a 9-digit integer.")
    
    return id


def validate_instructorID(id):
    """
    Validates the given instructor id.

    Args:
        id (string): The id to validate.

    Returns:
        string: The valid id.

    Raises:
        ValueError: If the id is not a 4 digit integer.
    """
    pattern = r'^\d{4}$'  # Regex pattern for 4-digit integers
    if not re.match(pattern, id):
        raise ValueError("Instructor ID must be a 4-digit integer.")
    
    return id


def validate_CourseID(id):
    """
    Validates the given course id.

    Args:
        id (string): The id to validate.

    Returns:
        string: The valid id.

    Raises:
        ValueError: If the id doesn't match the required format.
    """
    pattern = r'^[A-Z]{1,4}\d{3}[A-Z]?$'  
    if not re.match(pattern, id):
        raise ValueError("Invalid Course ID")
    
    return id


def validate_Student(student):
    """
    Validates the given student object.

    Args:
        student (Student): The student to validate.

    Returns:
        Student: The valid student.

    Raises:
        ValueError: If the student isn't a valid Student object.
    """
    if not isinstance(student, Student):
        raise ValueError("Invalid Student")
    
    return student


def validate_Instructor(instructor):
    """
    Validates the given instructor object.

    Args:
        instructor (Instructor): The instructor to validate.

    Returns:
        Instructor: The valid instructor.

    Raises:
        ValueError: If the instructor isn't a valid Instructor object.
    """
    if not isinstance(instructor, Instructor):
        raise ValueError("Invalid Instructor")
    
    return instructor


def validate_Course(course):
    """
    Validates the given course object.

    Args:
        course (Course): The course to validate.

    Returns:
        Course: The valid course.

    Raises:
        ValueError: If the course isn't a valid Course object.
    """
    if not isinstance(course, Course):
        raise ValueError("Invalid Course")
    
    return course


#Define the Person Class
class Person:
   def __init__(self, name, age, email):
       self.name = validate_name(name)
       self.age = validate_age(age)
       self.__email = validate_email(email)

   def introduce(self):
    """Prints a greeting introducing the person by name and age."""
    print(f"Hello, my name is {self.name}, and I am {self.age} years old.")


#Define the Student subclass
class Student(Person):
   def __init__(self, name, age, email, student_id):
       super().__init__(name, age, email)
       self.student_id = validate_studentID(student_id)
       self.registered_courses = []

   def register_course(self, course):
        """Registers a course for the student."""
        valid_course = validate_Course(course)
        self.registered_courses.append(valid_course)
        valid_course.add_student(self)

#Define the Instructor subclass
class Instructor(Person):
   def __init__(self, name, age, email, instructor_id):
       super().__init__(name, age, email)
       self.instructor_id = validate_instructorID(instructor_id)
       self.assigned_courses = []

   def assign_course(self, course):
       valid_course = validate_Course(course)
       self.assigned_courses.append(valid_course)


#Define the Course class
class Course:
    def __init__(self, course_id, course_name, instructor):
        self.course_id = validate_CourseID(course_id)
        self.course_name = course_name
        self.instructor = validate_Instructor(instructor)
        self.enrolled_students = []
    
    def add_student(self, student):
        valid_student = validate_Student(student)
        self.enrolled_students.append(valid_student)


#Serialization
def save_to_file(instructors, courses, students, fileName):
    """Saves instructor, course, and student data to a JSON file.

    Args:
        instructor (list of Instructor): List of instructor objects to serialize.
        courses (list of Course): List of course objects to serialize.
        students (list of Student): List of student objects to serialize.
        file_name (str): The name of the file to save data to.

    Raises:
        Exception: If there is an error in writing to the file.
    """
    # Prepare data for serialization
    data = {
        "Instructor": [
            {
                "Name": instructor.name,
                "Age": instructor.age,
                "Email": instructor._Person__email, 
                "InstructorID": instructor.instructor_id,
                "Assigned Courses": [course.course_id for course in instructor.assigned_courses]
    }
    for instructor in instructors  

        ],
        "Courses": [
            {
                "CourseID": course.course_id,
                "Course Name": course.course_name,
                "InstructorID": course.instructor.instructor_id,
                "Enrolled Students": [student.student_id for student in course.enrolled_students]
            }
            for course in courses  # Generates a dictionary for each course in the courses list
        ],
        "Students": [
            {
                "Name": student.name,
                "Age": student.age,
                "Email": student._Person__email,  
                "StudentID": student.student_id,
                "Registered Courses": [course.course_id for course in student.registered_courses]
            }
            for student in students  # Generates a dictionary for each student in the students list
        ]
    }

    # Write data to JSON file
    try:
        with open(fileName, 'w') as json_file:
            json.dump(data, json_file, indent=4)  # Indent for better readability
    except Exception as e:
        raise Exception(f"An error occurred while writing to the file: {e}")
    

#Deserialization
def load_from_file(fileName):
    """
    Loads data from a JSON file and creates instances of Instructor, Course, and Student.

    Parameters:
    - fileName (str): The name of the JSON file to load data from. The file should contain 
      structured data with sections for "Instructor", "Courses", and "Students".

    Returns:
    - tuple: A tuple containing three dictionaries:
        - Instructors_Dict (dict): A dictionary where keys are Instructor IDs and values are 
          Instructor objects.
        - Courses_Dict (dict): A dictionary where keys are Course IDs and values are 
          Course objects.
        - Students_Dict (dict): A dictionary where keys are Student IDs and values are 
          Student objects.

    The function performs the following steps:
    1. Opens and reads a JSON file specified by the `fileName` parameter.
    2. Parses the JSON data to create Instructor objects and stores them in `Instructors_Dict`.
    3. Parses the JSON data to create Course objects, linking each course to its respective 
       instructor from `Instructors_Dict`, and stores them in `Courses_Dict`.
    4. Parses the JSON data to create Student objects, registering each student in their 
       respective courses by updating both the student's registered courses and the course's 
       enrolled students.
    5. Assigns courses to instructors, ensuring that each instructor has a record of the 
       courses they teach.
    """
    with open(fileName, 'r') as file:
        data = json.load(file)
    
    Instructors_Dict = {}
    for instructors in data["Instructor"]:
        instructor = Instructor(instructors["Name"], instructors["Age"], instructors["Email"], instructors["InstructorID"])
        Instructors_Dict[instructor.instructor_id] = instructor

    Courses_Dict = {}
    for courses in data["Courses"]:
        course = Course(courses["CourseID"], courses["Course Name"], Instructors_Dict[courses["InstructorID"]])
        Courses_Dict[course.course_id] = course
    
    Students_Dict = {}
    for students in data["Students"]:
        student = Student(students["Name"], students["Age"], students["Email"], students["StudentID"])
        for registered in students["Registered Courses"]:
            student.register_course(Courses_Dict[registered]) # Register Student in course according to the Course ID
        Students_Dict[student.student_id] = student
    
    for course in Courses_Dict.values():
        Instructors_Dict[course.instructor.instructor_id].assign_course(course)
    
    for students in Students_Dict.values():
        for enrolled in students.registered_courses:
            Courses_Dict[enrolled.course_id].add_student(students)


    return Instructors_Dict, Courses_Dict, Students_Dict


if __name__ == "__main__":
# Create Instructor
    instructor1 = Instructor ("Alice", 40, "alice@aub.edu", "1000")
    instructor2 = Instructor ("Bobby", 29, "bobby@aub.edu", "1001")
    instructorList = [instructor1, instructor2]
    # Create Courses
    course1 = Course("CSE101", "Intro to Computer Science", instructor1)
    course2 = Course("CSE102", "Data Structures", instructor1)
    course3 = Course("EECE435L", "Software Tools Lab", instructor2)
    course4 = Course("EECE503G", "Ethical Hacking ", instructor2)
    # Assign courses to the instructors
    instructor1.assign_course(course1) 
    instructor1.assign_course(course2)
    instructor2.assign_course(course3)
    instructor2.assign_course(course4)
    # Create Student
    student = Student("Sammy", 20, "sna61@aub.edu", "202202056")
    # Register student in each course
    student.register_course(course1)
    student.register_course(course2)
    student.register_course(course3)
    student.register_course(course4)
    # Serialize
    save_to_file(instructorList, [course1, course2, course3, course4], [student], 'school_data.json')
    # Output example
    print("\nData saved to school_data.json\n")
    # Deserialization: Load from file
    instructors, courses, students = load_from_file("school_data.json")
    for instructor in instructorList:
        print(f"Instructor Name: {instructors[instructor.instructor_id].name}")
        assigned = [course.course_id for course in instructors[instructor.instructor_id].assigned_courses]
        print(f"Assigned Courses: {', '.join(assigned)}")
