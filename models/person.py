import re
from typing import Dict, Any
            
class Person:

    def __init__(self, name: str, age: int, email: str):
        self.name = name
        self.age = self._validate_age(age)
        self._email = self._validate_email(email)

    @staticmethod
    def _validate_name(name: str) -> str:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")
        return name.strip()
    
    @staticmethod
    def _validate_email(email: str) -> str:
        if not isinstance(email, str):
            raise ValueError("Email must be a string")
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")
        return email

    @staticmethod
    def _validate_age(age: int) -> int:
        if not isinstance(age, int) or age < 0:
            raise ValueError("Age must be a non-negative integer")
        if age > 150:
            raise ValueError("Age must be realistic (0-150)")
        return age

    def introduce(self) -> None:
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")

    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.__class__.__name__,
            'name': self.name,
            'age': self.age,
            'email': self._email
        }
    
    used_emails = set()
    used_ids = set()
