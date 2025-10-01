from models.person import Person
import re
from typing import Dict, Any, List


class Student(Person):

    def __init__(self, name, age, email, student_id):

        if email in Person.used_emails:
            raise ValueError(f"The email {email} already exists.")
        if student_id in Person.used_ids:
            raise ValueError(f"The ID '{student_id}' already exists.")

        super().__init__(name, age, email)
        self.student_id = self._validate_student_id(student_id)
        self.registered_courses = []

        Person.used_ids.add(student_id)
        Person.used_emails.add(email) 

    @staticmethod
    def _validate_student_id(student_id: str) -> str:

        if not isinstance(student_id, str) or not student_id.strip():
            raise ValueError("Student ID must be a non-empty string")
        
        if not re.match(r'^STU\d{3,}$', student_id):
            raise ValueError("Student ID must follow format 'STU' + at least 3 digits (e.g., STU001)")
        return student_id.upper()
    
    def register_course(self, course):

        from course import Course

        if not isinstance(course, Course):
            raise ValueError("course must be a Course object")
        
        if course not in self.registered_courses:
            self.registered_courses.append(course)
            course.add_student(self)
            print(f"{self.name} registered for {course.course_name}")
        else:
            print(f"{self.name} is already registered for {course.course_name}")

    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        base_dict.update({
            'student_id': self.student_id,
            'registered_courses': [course.course_id for course in self.registered_courses]
        })
        return base_dict