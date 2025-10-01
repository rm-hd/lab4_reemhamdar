import sys
import pickle
import csv
import re
from models.person import Person
from models.student import Student
from models.instructor import Instructor
from models.course import Course
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QLabel, QTextEdit, QTabWidget, QMessageBox, QComboBox
)


class SchoolManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 800, 600)

        self.students = []
        self.instructors = []
        self.courses = []

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.student_tab = QWidget()
        self.instructor_tab = QWidget()
        self.course_tab = QWidget()
        self.overview_tab = QWidget()

        self.tabs.addTab(self.student_tab, "Students")
        self.tabs.addTab(self.instructor_tab, "Instructors")
        self.tabs.addTab(self.course_tab, "Courses")
        self.tabs.addTab(self.overview_tab, "Overview")

        self.init_student_tab()
        self.init_instructor_tab()
        self.init_course_tab()
        self.init_overview_tab()

    # STUDENTS TAB
    def init_student_tab(self):
        layout = QVBoxLayout(self.student_tab)
        form_layout = QFormLayout()

        self.student_name_entry = QLineEdit(self.student_tab)
        self.student_age_entry = QLineEdit(self.student_tab)
        self.student_email_entry = QLineEdit(self.student_tab)
        self.student_id_entry = QLineEdit(self.student_tab)
        form_layout.addRow("Name", self.student_name_entry)
        form_layout.addRow("Age", self.student_age_entry)
        form_layout.addRow("Email", self.student_email_entry)
        form_layout.addRow("Student ID", self.student_id_entry)

        self.register_course_dropdown = QComboBox(self.student_tab)
        self.register_course_dropdown.addItem("None")
        form_layout.addRow("Select Course to Register", self.register_course_dropdown)

        self.add_student_button = QPushButton("Add Student")
        self.add_student_button.clicked.connect(self.add_student)
        self.delete_student_button = QPushButton("Delete Student")
        self.delete_student_button.clicked.connect(self.delete_student)

        layout.addLayout(form_layout)
        layout.addWidget(self.add_student_button)
        layout.addWidget(self.delete_student_button)

        self.student_tree = QTableWidget()
        self.student_tree.setColumnCount(5)
        self.student_tree.setHorizontalHeaderLabels(['ID', 'Name', 'Age', 'Email', 'Courses'])
        layout.addWidget(self.student_tree)

    # INSTRUCTORS TAB 
    def init_instructor_tab(self):
        layout = QVBoxLayout(self.instructor_tab)
        form_layout = QFormLayout()

        self.instructor_name_entry = QLineEdit(self.instructor_tab)
        self.instructor_age_entry = QLineEdit(self.instructor_tab)
        self.instructor_email_entry = QLineEdit(self.instructor_tab)
        self.instructor_id_entry = QLineEdit(self.instructor_tab)
        form_layout.addRow("Name", self.instructor_name_entry)
        form_layout.addRow("Age", self.instructor_age_entry)
        form_layout.addRow("Email", self.instructor_email_entry)
        form_layout.addRow("Instructor ID", self.instructor_id_entry)

        self.assign_course_dropdown = QComboBox(self.instructor_tab)
        self.assign_course_dropdown.addItem("None")
        form_layout.addRow("Select Course to Assign", self.assign_course_dropdown)

        self.add_instructor_button = QPushButton("Add Instructor")
        self.add_instructor_button.clicked.connect(self.add_instructor)
        self.delete_instructor_button = QPushButton("Delete Instructor")
        self.delete_instructor_button.clicked.connect(self.delete_instructor)

        layout.addLayout(form_layout)
        layout.addWidget(self.add_instructor_button)
        layout.addWidget(self.delete_instructor_button)

        self.instructor_tree = QTableWidget()
        self.instructor_tree.setColumnCount(5)
        self.instructor_tree.setHorizontalHeaderLabels(['ID', 'Name', 'Age', 'Email', 'Courses'])
        layout.addWidget(self.instructor_tree)

    # COURSES TAB 
    def init_course_tab(self):
        layout = QVBoxLayout(self.course_tab)
        form_layout = QFormLayout()

        self.course_id_entry = QLineEdit(self.course_tab)
        self.course_name_entry = QLineEdit(self.course_tab)
        form_layout.addRow("Course ID", self.course_id_entry)
        form_layout.addRow("Course Name", self.course_name_entry)

        self.add_course_button = QPushButton("Add Course")
        self.add_course_button.clicked.connect(self.add_course)
        self.edit_course_button = QPushButton("Edit Course")
        self.edit_course_button.clicked.connect(self.edit_course)
        self.save_course_button = QPushButton("Save Course")
        self.save_course_button.clicked.connect(self.save_course)
        self.delete_course_button = QPushButton("Delete Course")
        self.delete_course_button.clicked.connect(self.delete_course)

        layout.addLayout(form_layout)
        layout.addWidget(self.add_course_button)
        layout.addWidget(self.edit_course_button)
        layout.addWidget(self.save_course_button)
        layout.addWidget(self.delete_course_button)

        self.course_tree = QTableWidget()
        self.course_tree.setColumnCount(2)
        self.course_tree.setHorizontalHeaderLabels(['Course ID', 'Course Name'])
        layout.addWidget(self.course_tree)

        self.refresh_course_dropdowns()

    # OVERVIEW TAB 
    def init_overview_tab(self):
        layout = QVBoxLayout(self.overview_tab)
        self.search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_records)

        self.students_text = QTextEdit()
        self.instructors_text = QTextEdit()
        self.courses_text = QTextEdit()

        layout.addWidget(self.search_label)
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)
        layout.addWidget(QLabel("Students"))
        layout.addWidget(self.students_text)
        layout.addWidget(QLabel("Instructors"))
        layout.addWidget(self.instructors_text)
        layout.addWidget(QLabel("Courses"))
        layout.addWidget(self.courses_text)

        self.refresh_button = QPushButton("Refresh Overview")
        self.refresh_button.clicked.connect(self.refresh_overview)
        layout.addWidget(self.refresh_button)

        self.save_button = QPushButton("Save Data")
        self.save_button.clicked.connect(self.save_data_to_file)
        self.load_button = QPushButton("Load Data")
        self.load_button.clicked.connect(self.load_data_from_file)
        self.export_students_button = QPushButton("Export Students to CSV")
        self.export_students_button.clicked.connect(self.export_students_to_csv)
        self.export_instructors_button = QPushButton("Export Instructors to CSV")
        self.export_instructors_button.clicked.connect(self.export_instructors_to_csv)
        self.export_courses_button = QPushButton("Export Courses to CSV")
        self.export_courses_button.clicked.connect(self.export_courses_to_csv)

        layout.addWidget(self.save_button)
        layout.addWidget(self.load_button)
        layout.addWidget(self.export_students_button)
        layout.addWidget(self.export_instructors_button)
        layout.addWidget(self.export_courses_button)

    # CRUD FUNCTIONS 
    def add_student(self):
        try:
            name = self.student_name_entry.text()
            age = int(self.student_age_entry.text())
            email = self.student_email_entry.text()
            student_id = self.student_id_entry.text()
            course_name = self.register_course_dropdown.currentText()

            if not name or not student_id:
                raise ValueError("Name and ID are required.")

            student = Student(name, age, email, student_id)
            if course_name != "None":
                student.courses.append(course_name)

            self.students.append(student)
            self.student_tree.insertRow(self.student_tree.rowCount())
            self.student_tree.setItem(self.student_tree.rowCount()-1, 0, QTableWidgetItem(student.student_id))
            self.student_tree.setItem(self.student_tree.rowCount()-1, 1, QTableWidgetItem(student.name))
            self.student_tree.setItem(self.student_tree.rowCount()-1, 2, QTableWidgetItem(str(student.age)))
            self.student_tree.setItem(self.student_tree.rowCount()-1, 3, QTableWidgetItem(student.get_email()))
            self.student_tree.setItem(self.student_tree.rowCount()-1, 4, QTableWidgetItem(", ".join(student.courses)))

            self.student_name_entry.clear()
            self.student_age_entry.clear()
            self.student_email_entry.clear()
            self.student_id_entry.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def delete_student(self):
        row = self.student_tree.currentRow()
        if row >= 0:
            self.student_tree.removeRow(row)
            del self.students[row]

    def add_instructor(self):
        try:
            name = self.instructor_name_entry.text()
            age = int(self.instructor_age_entry.text())
            email = self.instructor_email_entry.text()
            instructor_id = self.instructor_id_entry.text()
            course_name = self.assign_course_dropdown.currentText()

            if not name or not instructor_id:
                raise ValueError("Name and ID are required.")

            instructor = Instructor(name, age, email, instructor_id)
            if course_name != "None":
                instructor.courses.append(course_name)

            self.instructors.append(instructor)
            self.instructor_tree.insertRow(self.instructor_tree.rowCount())
            self.instructor_tree.setItem(self.instructor_tree.rowCount()-1, 0, QTableWidgetItem(instructor.instructor_id))
            self.instructor_tree.setItem(self.instructor_tree.rowCount()-1, 1, QTableWidgetItem(instructor.name))
            self.instructor_tree.setItem(self.instructor_tree.rowCount()-1, 2, QTableWidgetItem(str(instructor.age)))
            self.instructor_tree.setItem(self.instructor_tree.rowCount()-1, 3, QTableWidgetItem(instructor.get_email()))
            self.instructor_tree.setItem(self.instructor_tree.rowCount()-1, 4, QTableWidgetItem(", ".join(instructor.courses)))

            self.instructor_name_entry.clear()
            self.instructor_age_entry.clear()
            self.instructor_email_entry.clear()
            self.instructor_id_entry.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def delete_instructor(self):
        row = self.instructor_tree.currentRow()
        if row >= 0:
            self.instructor_tree.removeRow(row)
            del self.instructors[row]

    def add_course(self):
        try:
            course_id = self.course_id_entry.text()
            course_name = self.course_name_entry.text()

            if not course_id or not course_name:
                raise ValueError("Course ID and Name are required.")

            course = Course(course_id, course_name)
            self.courses.append(course)
            self.course_tree.insertRow(self.course_tree.rowCount())
            self.course_tree.setItem(self.course_tree.rowCount()-1, 0, QTableWidgetItem(course.course_id))
            self.course_tree.setItem(self.course_tree.rowCount()-1, 1, QTableWidgetItem(course.course_name))

            self.course_id_entry.clear()
            self.course_name_entry.clear()
            self.refresh_course_dropdowns()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def edit_course(self):
        selected_row = self.course_tree.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a course to edit.")
            return
        self.course_id_entry.setText(self.course_tree.item(selected_row, 0).text())
        self.course_name_entry.setText(self.course_tree.item(selected_row, 1).text())
        self.add_course_button.setDisabled(True)
        self.save_course_button.setEnabled(True)

    def save_course(self):
        course_id = self.course_id_entry.text()
        course_name = self.course_name_entry.text()
        for course in self.courses:
            if course.course_id == course_id:
                course.course_name = course_name
        selected_row = self.course_tree.currentRow()
        self.course_tree.setItem(selected_row, 1, QTableWidgetItem(course_name))
        self.add_course_button.setEnabled(True)
        self.save_course_button.setDisabled(True)
        QMessageBox.information(self, "Success", "Course updated successfully.")

    def delete_course(self):
        row = self.course_tree.currentRow()
        if row >= 0:
            self.course_tree.removeRow(row)
            del self.courses[row]
            self.refresh_course_dropdowns()

    # OVERVIEW FUNCTIONS 
    def search_records(self):
        search_text = self.search_input.text().lower()
        self.students_text.clear()
        self.instructors_text.clear()
        self.courses_text.clear()
        filtered_students = [f"{s.name} ({s.student_id}) - {', '.join(s.courses)}" 
                             for s in self.students if search_text in s.name.lower() or search_text in s.student_id.lower()]
        filtered_instructors = [f"{i.name} ({i.instructor_id}) - {', '.join(i.courses)}" 
                                for i in self.instructors if search_text in i.name.lower() or search_text in i.instructor_id.lower()]
        filtered_courses = [f"{c.course_name} ({c.course_id})" 
                            for c in self.courses if search_text in c.course_name.lower() or search_text in c.course_id.lower()]
        self.students_text.append("\n".join(filtered_students) if filtered_students else "No matching students found.")
        self.instructors_text.append("\n".join(filtered_instructors) if filtered_instructors else "No matching instructors found.")
        self.courses_text.append("\n".join(filtered_courses) if filtered_courses else "No matching courses found.")

    def refresh_overview(self):
        self.students_text.clear()
        self.instructors_text.clear()
        self.courses_text.clear()
        self.students_text.append("\n".join([f"{s.name} ({s.student_id}) - {', '.join(s.courses)}" for s in self.students]))
        self.instructors_text.append("\n".join([f"{i.name} ({i.instructor_id}) - {', '.join(i.courses)}" for i in self.instructors]))
        self.courses_text.append("\n".join([f"{c.course_name} ({c.course_id})" for c in self.courses]))

    # FILE OPS 
    def save_data_to_file(self):
        try:
            with open("school_data.pkl", "wb") as f:
                pickle.dump({
                    "students": [s.to_dict() for s in self.students],
                    "instructors": [i.to_dict() for i in self.instructors],
                    "courses": [c.to_dict() for c in self.courses]
                }, f)
            QMessageBox.information(self, "Success", "Data saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def load_data_from_file(self):
        try:
            with open("school_data.pkl", "rb") as f:
                data = pickle.load(f)
                self.students = [Student.from_dict(s) for s in data["students"]]
                self.instructors = [Instructor.from_dict(i) for i in data["instructors"]]
                self.courses = [Course.from_dict(c) for c in data["courses"]]

            self.refresh_overview()
            QMessageBox.information(self, "Success", "Data loaded successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def export_students_to_csv(self):
        try:
            with open("students.csv", "w", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["student_id", "name", "age", "email", "courses"])
                writer.writeheader()
                for s in self.students:
                    writer.writerow({"student_id": s.student_id, "name": s.name, "age": s.age,
                                     "email": s.get_email(), "courses": ", ".join(s.courses)})
            QMessageBox.information(self, "Success", "Students exported to students.csv.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def export_instructors_to_csv(self):
        try:
            with open("instructors.csv", "w", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["instructor_id", "name", "age", "email", "courses"])
                writer.writeheader()
                for i in self.instructors:
                    writer.writerow({"instructor_id": i.instructor_id, "name": i.name, "age": i.age,
                                     "email": i.get_email(), "courses": ", ".join(i.courses)})
            QMessageBox.information(self, "Success", "Instructors exported to instructors.csv.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def export_courses_to_csv(self):
        try:
            with open("courses.csv", "w", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["course_id", "course_name"])
                writer.writeheader()
                for c in self.courses:
                    writer.writerow({"course_id": c.course_id, "course_name": c.course_name})
            QMessageBox.information(self, "Success", "Courses exported to courses.csv.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # === HELPERS ===
    def refresh_course_dropdowns(self):
        self.register_course_dropdown.clear()
        self.register_course_dropdown.addItem("None")
        self.assign_course_dropdown.clear()
        self.assign_course_dropdown.addItem("None")
        for c in self.courses:
            self.register_course_dropdown.addItem(c.course_name)
            self.assign_course_dropdown.addItem(c.course_name)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SchoolManagementApp()
    window.show()
    sys.exit(app.exec_())