import re
from typing import Dict, Any, List, Optional, Tuple
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from instructor import Instructor

class Course:

    existing_course_ids = set()

    def __init__(self, course_id: str, course_name: str, instructor=None):

        if course_id in Course.existing_course_ids:
            raise ValueError(f"Course ID '{course_id}' already exists.")
        
        self.course_id = self._validate_course_id(course_id)
        self.course_name = self._validate_course_name(course_name)
        self.instructor = self._validate_instructor(instructor)
        self.enrolled_students = []  

        if instructor:
            instructor.assign_course(self)

        Course.existing_course_ids.add(course_id)


    @staticmethod
    def _validate_course_id(course_id: str) -> str:

        if not isinstance(course_id, str) or not course_id.strip():
            raise ValueError("Course ID must be a non-empty string")

        if not re.match(r'^[A-Z]{2,4}\d{3}$', course_id):
            raise ValueError("Course ID must follow format: 2-4 letters + 3 digits (e.g., CS101)")
        return course_id.upper()

    @staticmethod
    def _validate_course_name(course_name: str) -> str:

        if not isinstance(course_name, str) or not course_name.strip():
            raise ValueError("Course name must be a non-empty string")
        return course_name.strip()

    @staticmethod
    def _validate_instructor(instructor: Optional['Instructor']) -> Optional['Instructor']:

        if instructor is not None:
            from instructor import Instructor
            if not isinstance(instructor, Instructor):
                raise ValueError("instructor must be an Instructor object or None")
        return instructor

    def add_student(self, student):
       
        from student import Student
        
        if not isinstance(student, Student):
            raise ValueError("student must be a Student object")
        
        if student not in self.enrolled_students:
            self.enrolled_students.append(student)    

    def to_dict(self) -> Dict[str, Any]:
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'instructor_id': self.instructor.instructor_id if self.instructor else None,
            'enrolled_students': [student.student_id for student in self.enrolled_students]
        }