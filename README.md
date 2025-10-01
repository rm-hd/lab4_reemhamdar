Lab 4 - School Management System
Project Description
This project demonstrates the implementation of a comprehensive School Management System using two different Python GUI frameworks:

Tkinter: Python's standard GUI library
PyQt5: A more advanced Qt-based GUI framework

Both implementations provide the same functionality for managing students, instructors, and courses in an educational institution.
Features

Student Management: Add, edit, delete, and view student records with course registration
Instructor Management: Add, edit, delete, and assign instructors to courses
Course Management: Create and manage courses with instructor and student enrollment tracking
Search Functionality: Search across all records (students, instructors, courses)
Data Persistence: Save and load data using JSON/Pickle format
CSV Export: Export student, instructor, and course data to CSV files
Email Validation: Automatic validation of email formats
ID Format Validation: Enforces proper ID formats (STU### for students, INST### for instructors, XXNNN for courses)
Tabbed Interface: Easy navigation between different management sections

Project Structure
Lab4-SchoolManagement/
├── tkinter_app.py              # Tkinter implementation
├── pyqt_app.py                 # PyQt5 implementation
├── models/
│   ├── person.py              # Base Person class
│   ├── student.py             # Student class
│   ├── instructor.py          # Instructor class
│   └── course.py              # Course class
├── UniversityDataManager.py    # Data management utilities
└── README.md                   # Project documentation
Requirements
For Tkinter Version:

Python 3.x
tkinter (usually comes pre-installed with Python)

For PyQt Version:

Python 3.x
PyQt5 or PyQt6

Install PyQt5 using:
bashpip install PyQt5
Or for PyQt6:
bashpip install PyQt6
How to Run
Running the Tkinter Version:
bashpython tkinter_app.py
Running the PyQt Version:
bashpython pyqt_app.py
Development Process
This project was developed using Git version control with the following workflow:

Created separate branches for each implementation (feature-tkinter and feature-pyqt)
Developed and committed changes independently on each branch
Merged both branches into the master/main branch
Tagged the final version as v1.0

Version History

v1.0 - Initial release with both Tkinter and PyQt implementations

Author
Reem Hamdar

Course: Software Tools Lab
Semester: Fall 2024-2025
Lab: Lab 4 - Version Control, Git and GitHub

License
This project is submitted as part of coursework for educational purposes.