from models.person import Person
import re
from typing import Dict, Any, List, Optional, Tuple

class Instructor(Person):

    def __init__(self, name, age, email, instructor_id):

        if email in Person.used_emails:
            raise ValueError(f"The email {email} already exists.")
        if instructor_id in Person.used_ids:
            raise ValueError(f"The ID '{instructor_id}' already exists.")

        super().__init__(name, age, email)
        self.instructor_id = self._validate_instructor_id(instructor_id)
        self.assigned_courses = []  # List of Course objects

        Person.used_ids.add(instructor_id)
        Person.used_emails.add(email)
    
    @staticmethod
    def _validate_instructor_id(instructor_id: str) -> str:

        if not isinstance(instructor_id, str) or not instructor_id.strip():
            raise ValueError("Instructor ID must be a non-empty string")
        
        if not re.match(r'^INST\d{3,}$', instructor_id):
            raise ValueError("Instructor ID must follow format 'INST' + at least 3 digits (e.g., INST001)")
        return instructor_id.upper()
    
    
    def assign_course(self, course):

        from course import Course
        
        if not isinstance(course, Course):
            raise ValueError("course must be a Course object")
        
        if course not in self.assigned_courses:
            self.assigned_courses.append(course)
            print(f"{self.name} assigned to teach {course.course_name}")
        else:
            print(f"{self.name} is already assigned to {course.course_name}")
    
    def to_dict(self) -> Dict[str, Any]:    

        base_dict = super().to_dict()
        base_dict.update({
            'instructor_id': self.instructor_id,
            'assigned_courses': [course.course_id for course in self.assigned_courses]
        })
        return base_dict