import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re
from models.student import Student
from models.instructor import Instructor
from models.course import Course
from UniversityDataManager import UniversityDataManager 


class SchoolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("School Management System")
        self.root.geometry("900x600")
        self.students, self.instructors, self.courses = [], [], []
        self.editing_item = None

        self.notebook = ttk.Notebook(root)
        self.setup_tabs()
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

    def setup_tabs(self):
        self.student_tab = ttk.Frame(self.notebook)
        self.instructor_tab = ttk.Frame(self.notebook)
        self.course_tab = ttk.Frame(self.notebook)
        self.overview_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.student_tab, text="Students")
        self.notebook.add(self.instructor_tab, text="Instructors")
        self.notebook.add(self.course_tab, text="Courses")
        self.notebook.add(self.overview_tab, text="Overview")
        
        self.setup_student_tab()
        self.setup_instructor_tab()
        self.setup_course_tab()
        self.setup_overview_tab()

    # Student Tab 
    def setup_student_tab(self):
        # Form
        form = ttk.LabelFrame(self.student_tab, text="Student Information", padding=10)
        form.pack(fill="x", padx=5, pady=5)
        
        fields = [("Name", "st_name"), ("Age", "st_age"), ("Email", "st_email"), ("Student ID", "st_id")]
        for i, (label, attr) in enumerate(fields):
            ttk.Label(form, text=label).grid(row=i, column=0, sticky="w", padx=5)
            entry = ttk.Entry(form, width=25)
            entry.grid(row=i, column=1, padx=5, pady=2)
            setattr(self, attr, entry)
        
        ttk.Label(form, text="Course").grid(row=4, column=0, sticky="w", padx=5)
        self.st_course = ttk.Combobox(form, state="readonly", width=22)
        self.st_course.grid(row=4, column=1, padx=5, pady=2)
        
        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Add", command=self.add_student).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Edit", command=lambda: self.edit_record("student")).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Delete", command=lambda: self.delete_record("student")).pack(side="left", padx=2)
        
        self.student_tree = ttk.Treeview(self.student_tab, columns=("ID", "Name", "Age", "Email", "Courses"), show="headings", height=12)
        for col in ("ID", "Name", "Age", "Email", "Courses"):
            self.student_tree.heading(col, text=col)
        self.student_tree.pack(fill="both", expand=True, padx=5, pady=5)

    def add_student(self):
        try:
            name, age, email, sid = [field.get().strip() for field in [self.st_name, self.st_age, self.st_email, self.st_id]]
            
            if not all([name, age, email, sid]):
                raise ValueError("All fields required")
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                raise ValueError("Invalid email format")
            if not re.match(r'^STU\d{3,}$', sid.upper()):
                raise ValueError("Student ID format: STU + 3+ digits")
            
            student = Student(name, int(age), email, sid.upper())
            
            course_name = self.st_course.get()
            if course_name:
                course = next((c for c in self.courses if c.course_name == course_name), None)
                if course:
                    student.register_course(course)
            
            self.students.append(student)
            self.refresh_all()
            self.clear_form([self.st_name, self.st_age, self.st_email, self.st_id])
            messagebox.showinfo("Success", "Student added!")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # Instructor Tab 
    def setup_instructor_tab(self):
        form = ttk.LabelFrame(self.instructor_tab, text="Instructor Information", padding=10)
        form.pack(fill="x", padx=5, pady=5)
        
        fields = [("Name", "inst_name"), ("Age", "inst_age"), ("Email", "inst_email"), ("Instructor ID", "inst_id")]
        for i, (label, attr) in enumerate(fields):
            ttk.Label(form, text=label).grid(row=i, column=0, sticky="w", padx=5)
            entry = ttk.Entry(form, width=25)
            entry.grid(row=i, column=1, padx=5, pady=2)
            setattr(self, attr, entry)
        
        ttk.Label(form, text="Course").grid(row=4, column=0, sticky="w", padx=5)
        self.inst_course = ttk.Combobox(form, state="readonly", width=22)
        self.inst_course.grid(row=4, column=1, padx=5, pady=2)
        
        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Add", command=self.add_instructor).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Edit", command=lambda: self.edit_record("instructor")).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Delete", command=lambda: self.delete_record("instructor")).pack(side="left", padx=2)
        
        self.instructor_tree = ttk.Treeview(self.instructor_tab, columns=("ID", "Name", "Age", "Email", "Courses"), show="headings", height=12)
        for col in ("ID", "Name", "Age", "Email", "Courses"):
            self.instructor_tree.heading(col, text=col)
        self.instructor_tree.pack(fill="both", expand=True, padx=5, pady=5)

    def add_instructor(self):
        try:
            name, age, email, iid = [field.get().strip() for field in [self.inst_name, self.inst_age, self.inst_email, self.inst_id]]
            
            if not all([name, age, email, iid]):
                raise ValueError("All fields required")
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                raise ValueError("Invalid email format")
            if not re.match(r'^INST\d{3,}$', iid.upper()):
                raise ValueError("Instructor ID format: INST + 3+ digits")
            
            instructor = Instructor(name, int(age), email, iid.upper())
            
            course_name = self.inst_course.get()
            if course_name:
                course = next((c for c in self.courses if c.course_name == course_name), None)
                if course:
                    instructor.assign_course(course)
                    course.instructor = instructor
            
            self.instructors.append(instructor)
            self.refresh_all()
            self.clear_form([self.inst_name, self.inst_age, self.inst_email, self.inst_id])
            messagebox.showinfo("Success", "Instructor added!")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # ---------- Course Tab ----------
    def setup_course_tab(self):
        form = ttk.LabelFrame(self.course_tab, text="Course Information", padding=10)
        form.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(form, text="Course ID").grid(row=0, column=0, sticky="w", padx=5)
        self.crs_id = ttk.Entry(form, width=25)
        self.crs_id.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(form, text="Course Name").grid(row=1, column=0, sticky="w", padx=5)
        self.crs_name = ttk.Entry(form, width=25)
        self.crs_name.grid(row=1, column=1, padx=5, pady=2)
        
        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Add", command=self.add_course).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Edit", command=lambda: self.edit_record("course")).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Delete", command=lambda: self.delete_record("course")).pack(side="left", padx=2)
        
        self.course_tree = ttk.Treeview(self.course_tab, columns=("ID", "Name", "Instructor", "Students"), show="headings", height=12)
        for col in ("ID", "Name", "Instructor", "Students"):
            self.course_tree.heading(col, text=col)
        self.course_tree.pack(fill="both", expand=True, padx=5, pady=5)

    def add_course(self):
        try:
            cid, name = self.crs_id.get().strip(), self.crs_name.get().strip()
            
            if not all([cid, name]):
                raise ValueError("Course ID and Name required")
            if not re.match(r'^[A-Z]{2,4}\d{3}$', cid.upper()):
                raise ValueError("Course ID format: 2-4 letters + 3 digits")
            
            course = Course(cid.upper(), name)
            self.courses.append(course)
            self.refresh_all()
            self.clear_form([self.crs_id, self.crs_name])
            messagebox.showinfo("Success", "Course added!")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # ---------- Overview Tab ----------
    def setup_overview_tab(self):
        search_frame = ttk.LabelFrame(self.overview_tab, text="Search", padding=10)
        search_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(search_frame, text="Search:").grid(row=0, column=0)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.grid(row=0, column=1, padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_records).grid(row=0, column=2, padx=5)
        
        self.overview_text = tk.Text(self.overview_tab, wrap="word", height=15)
        self.overview_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        btn_frame = ttk.Frame(self.overview_tab)
        btn_frame.pack(fill="x", padx=5, pady=5)
        
        for text, cmd in [("Refresh", self.refresh_overview), ("Save", self.save_data), ("Load", self.load_data), ("Export", self.export_csv)]:
            ttk.Button(btn_frame, text=text, command=cmd).pack(side="left", padx=2)

    def search_records(self):
        term = self.search_entry.get().lower()
        if not term:
            return
        
        results = []
        
        for s in self.students:
            if term in s.name.lower() or term in s.student_id.lower() or term in s._email.lower():
                courses = ", ".join([c.course_name for c in s.registered_courses]) or "None"
                results.append(f"Student: {s.name} ({s.student_id}) - Courses: {courses}")
        
        for i in self.instructors:
            if term in i.name.lower() or term in i.instructor_id.lower() or term in i._email.lower():
                courses = ", ".join([c.course_name for c in i.assigned_courses]) or "None"
                results.append(f"Instructor: {i.name} ({i.instructor_id}) - Courses: {courses}")
        
        for c in self.courses:
            if term in c.course_name.lower() or term in c.course_id.lower():
                instructor = c.instructor.name if c.instructor else "None"
                results.append(f"Course: {c.course_name} ({c.course_id}) - Instructor: {instructor}")
        
        self.overview_text.delete(1.0, tk.END)
        self.overview_text.insert(tk.END, "\n".join(results) if results else "No results found")

    def refresh_overview(self):
        text = ""
        text += "=== STUDENTS ===\n"
        for s in self.students:
            courses = ", ".join([c.course_name for c in s.registered_courses]) or "None"
            text += f"{s.student_id}: {s.name}, Age {s.age}, Courses: {courses}\n"
        
        text += "\n=== INSTRUCTORS ===\n"
        for i in self.instructors:
            courses = ", ".join([c.course_name for c in i.assigned_courses]) or "None"
            text += f"{i.instructor_id}: {i.name}, Age {i.age}, Courses: {courses}\n"
        
        text += "\n=== COURSES ===\n"
        for c in self.courses:
            instructor = c.instructor.name if c.instructor else "None"
            students = ", ".join([s.name for s in c.enrolled_students]) or "None"
            text += f"{c.course_id}: {c.course_name}, Instructor: {instructor}, Students: {students}\n"
        
        self.overview_text.delete(1.0, tk.END)
        self.overview_text.insert(tk.END, text)

    # Generic Edit/Delete 
    def edit_record(self, record_type):
        trees = {"student": self.student_tree, "instructor": self.instructor_tree, "course": self.course_tree}
        tree = trees[record_type]
        
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", f"Select a {record_type} to edit")
            return
        
        values = tree.item(selection[0], 'values')
        
        if record_type == "student":
            fields = [self.st_id, self.st_name, self.st_age, self.st_email]
        elif record_type == "instructor":
            fields = [self.inst_id, self.inst_name, self.inst_age, self.inst_email]
        else:  # course
            fields = [self.crs_id, self.crs_name]
        
        for field, value in zip(fields, values):
            field.delete(0, tk.END)
            field.insert(0, value)
        
        self.editing_item = (record_type, values[0])  # Store type and ID

    def delete_record(self, record_type):
        trees = {"student": self.student_tree, "instructor": self.instructor_tree, "course": self.course_tree}
        tree = trees[record_type]
        
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", f"Select a {record_type} to delete")
            return
        
        values = tree.item(selection[0], 'values')
        if not messagebox.askyesno("Confirm", f"Delete {record_type} {values[1]} ({values[0]})?"):
            return
        
        if record_type == "student":
            self.students = [s for s in self.students if s.student_id != values[0]]
        elif record_type == "instructor":
            self.instructors = [i for i in self.instructors if i.instructor_id != values[0]]
        else:  
            self.courses = [c for c in self.courses if c.course_id != values[0]]
        
        self.refresh_all()
        messagebox.showinfo("Success", f"{record_type.title()} deleted!")

    # Utilities 
    def refresh_all(self):
        for tree in [self.student_tree, self.instructor_tree, self.course_tree]:
            tree.delete(*tree.get_children())
        
        for s in self.students:
            courses = ", ".join([c.course_name for c in s.registered_courses]) or "None"
            self.student_tree.insert("", "end", values=(s.student_id, s.name, s.age, s._email, courses))
        
        for i in self.instructors:
            courses = ", ".join([c.course_name for c in i.assigned_courses]) or "None"
            self.instructor_tree.insert("", "end", values=(i.instructor_id, i.name, i.age, i._email, courses))
        
        for c in self.courses:
            instructor = c.instructor.name if c.instructor else "None"
            students = ", ".join([s.name for s in c.enrolled_students]) or "None"
            self.course_tree.insert("", "end", values=(c.course_id, c.course_name, instructor, students))
        
        course_names = [c.course_name for c in self.courses]
        self.st_course['values'] = course_names
        self.inst_course['values'] = course_names

    def clear_form(self, fields):
        for field in fields:
            field.delete(0, tk.END)

    def save_data(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            UniversityDataManager.save_to_json(filename, self.students, self.instructors, self.courses)
            messagebox.showinfo("Success", "Data saved!")

    def load_data(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            students_dict, instructors_dict, courses_dict = UniversityDataManager.load_from_json(filename)
            self.students = list(students_dict.values())
            self.instructors = list(instructors_dict.values())
            self.courses = list(courses_dict.values())
            self.refresh_all()
            messagebox.showinfo("Success", "Data loaded!")

    def export_csv(self):
        import csv
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Type", "ID", "Name", "Age", "Email", "Details"])
                for s in self.students:
                    courses = ", ".join([c.course_name for c in s.registered_courses])
                    writer.writerow(["Student", s.student_id, s.name, s.age, s._email, courses])
                for i in self.instructors:
                    courses = ", ".join([c.course_name for c in i.assigned_courses])
                    writer.writerow(["Instructor", i.instructor_id, i.name, i.age, i._email, courses])
            messagebox.showinfo("Success", "Data exported!")


if __name__ == "__main__":
    root = tk.Tk()
    app = SchoolApp(root)
    root.mainloop()