import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['enrollment_db']

students_collection = db['students']
courses_collection = db['courses']
enrollments_collection = db['enrollments']
students_collection.create_index('email', unique=True)
courses_collection.create_index('course_id', unique=True)

root = tk.Tk()
root.title("Enrollment Management System")
root.geometry("1200x700")
root.config(bg="#f7f9fc")

def clear_fields():
    for entry in [first_name, last_name, email, dob, major, 
                  course_id, course_name, department, 
                  credits, instructor, semester]:
        entry.delete(0, tk.END)

def add_student():
    fname = first_name.get()
    lname = last_name.get()
    student_email = email.get()
    student_dob = dob.get()
    student_major = major.get()

    if fname and lname and student_email:
        try:
            student_data = {
                'first_name': fname,
                'last_name': lname,
                'email': student_email,
                'date_of_birth': student_dob,
                'major': student_major,
                'enrollment_date': datetime.now()
            }
            students_collection.insert_one(student_data)
            load_students()
            messagebox.showinfo("Success", "Student added successfully!")
            clear_fields()
        except Exception as err:
            messagebox.showerror("Database Error", str(err))
    else:
        messagebox.showwarning("Input Error", "All fields are required.")

def update_student():
    selected = student_table.focus()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a student to update.")
        return

    student_data = student_table.item(selected, 'values')
    student_id = student_data[0]

    fname = simpledialog.askstring("Update", "Enter First Name:", initialvalue=student_data[1])
    lname = simpledialog.askstring("Update", "Enter Last Name:", initialvalue=student_data[2])
    student_email = simpledialog.askstring("Update", "Enter Email:", initialvalue=student_data[3])
    student_dob = simpledialog.askstring("Update", "Enter Date of Birth:", initialvalue=student_data[4])
    student_major = simpledialog.askstring("Update", "Enter Major:", initialvalue=student_data[5])

    if fname and lname and student_email:
        try:
            students_collection.update_one(
                {'_id': ObjectId(student_id)},
                {'$set': {
                    'first_name': fname, 
                    'last_name': lname, 
                    'email': student_email,
                    'date_of_birth': student_dob, 
                    'major': student_major
                }}
            )
            load_students()
            messagebox.showinfo("Success", "Student updated successfully!")
        except Exception as err:
            messagebox.showerror("Database Error", str(err))

def delete_student():
    selected = student_table.focus()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a student to delete.")
        return

    student_data = student_table.item(selected, 'values')
    student_id = student_data[0]

    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student? This will also remove all their enrollments."):
        try:
            enrollments_collection.delete_many({'student_id': ObjectId(student_id)})
            students_collection.delete_one({'_id': ObjectId(student_id)})
            
            load_students()
            load_enrollments()
            messagebox.showinfo("Success", "Student deleted successfully!")
        except Exception as err:
            messagebox.showerror("Database Error", str(err))

def add_course():
    cid = course_id.get()
    cname = course_name.get()
    cdepartment = department.get()
    ccredits = credits.get()
    cinstructor = instructor.get()

    if cid and cname and cdepartment and ccredits:
        try:
            course_data = {
                'course_id': cid,
                'course_name': cname,
                'department': cdepartment,
                'credits': int(ccredits),
                'instructor': cinstructor
            }
            courses_collection.insert_one(course_data)
            load_courses()
            messagebox.showinfo("Success", "Course added successfully!")
            clear_fields()
        except Exception as err:
            messagebox.showerror("Database Error", str(err))
    else:
        messagebox.showwarning("Input Error", "All course fields are required.")

def update_course():
    selected = course_table.focus()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a course to update.")
        return

    course_data = course_table.item(selected, 'values')
    course_id_val = course_data[0]

    cname = simpledialog.askstring("Update", "Enter Course Name:", initialvalue=course_data[1])
    cdepartment = simpledialog.askstring("Update", "Enter Department:", initialvalue=course_data[2])
    ccredits = simpledialog.askinteger("Update", "Enter Credits:", initialvalue=course_data[3])
    cinstructor = simpledialog.askstring("Update", "Enter Instructor:", initialvalue=course_data[4])

    if cname and cdepartment and ccredits and cinstructor:
        try:
            courses_collection.update_one(
                {'course_id': course_id_val},
                {'$set': {
                    'course_name': cname, 
                    'department': cdepartment, 
                    'credits': ccredits, 
                    'instructor': cinstructor
                }}
            )
            load_courses()
            messagebox.showinfo("Success", "Course updated successfully!")
        except Exception as err:
            messagebox.showerror("Database Error", str(err))

def delete_course():
    selected = course_table.focus()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a course to delete.")
        return

    course_data = course_table.item(selected, 'values')
    course_id_val = course_data[0]

    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this course? This will also remove all enrollments for this course."):
        try:
            enrollments_collection.delete_many({'course_id': course_id_val})
            courses_collection.delete_one({'course_id': course_id_val})
            
            load_courses()
            load_enrollments()
            messagebox.showinfo("Success", "Course deleted successfully!")
        except Exception as err:
            messagebox.showerror("Database Error", str(err))

def add_enrollment():
    student_selection = student_table.focus()
    course_selection = course_table.focus()
    
    if not student_selection or not course_selection:
        messagebox.showwarning("Selection Error", "Please select both a student and a course.")
        return

    student_data = student_table.item(student_selection, 'values')
    course_data = course_table.item(course_selection, 'values')
    
    student_id = student_data[0]
    course_id_val = course_data[0]
    sem = semester.get()

    if sem:
        try:
            enrollment_data = {
                'student_id': ObjectId(student_id),
                'course_id': course_id_val,
                'semester': sem,
                'enrollment_date': datetime.now(),
                'grade': None
            }
            enrollments_collection.insert_one(enrollment_data)
            messagebox.showinfo("Success", "Student enrolled successfully!")
            clear_fields()
            load_enrollments()
        except Exception as err:
            messagebox.showerror("Database Error", str(err))
    else:
        messagebox.showwarning("Input Error", "Semester is required.")

def update_enrollment():
    selected = enrollment_table.focus()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select an enrollment to update.")
        return

    enrollment_data = enrollment_table.item(selected, 'values')
    enrollment_id = enrollment_data[0]

    sem = simpledialog.askstring("Update", "Enter Semester:", initialvalue=enrollment_data[3])
    grade = simpledialog.askstring("Update", "Enter Grade (A/B/C/D/F/Incomplete):", initialvalue=enrollment_data[5] or '')

    if sem:
        try:
            enrollments_collection.update_one(
                {'_id': ObjectId(enrollment_id)},
                {'$set': {
                    'semester': sem, 
                    'grade': grade or None
                }}
            )
            load_enrollments()
            messagebox.showinfo("Success", "Enrollment updated successfully!")
        except Exception as err:
            messagebox.showerror("Database Error", str(err))

def delete_enrollment():
    selected = enrollment_table.focus()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select an enrollment to delete.")
        return

    enrollment_data = enrollment_table.item(selected, 'values')
    enrollment_id = enrollment_data[0]

    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this enrollment?"):
        try:
            enrollments_collection.delete_one({'_id': ObjectId(enrollment_id)})
            load_enrollments()
            messagebox.showinfo("Success", "Enrollment deleted successfully!")
        except Exception as err:
            messagebox.showerror("Database Error", str(err))

def load_students():
    for row in student_table.get_children():
        student_table.delete(row)
    pipeline = [
        {
            '$lookup': {
                'from': 'enrollments',
                'localField': '_id',
                'foreignField': 'student_id',
                'as': 'enrollments'
            }
        },
        {
            '$addFields': {
                'total_courses': {'$size': '$enrollments'},
                'gwa': {
                    '$avg': {
                        '$map': {
                            'input': '$enrollments',
                            'as': 'enrollment',
                            'in': {
                                '$switch': {
                                    'branches': [
                                        {'case': {'$eq': ['$$enrollment.grade', 'A']}, 'then': 1.0},
                                        {'case': {'$eq': ['$$enrollment.grade', 'B']}, 'then': 2.0},
                                        {'case': {'$eq': ['$$enrollment.grade', 'C']}, 'then': 3.0},
                                        {'case': {'$eq': ['$$enrollment.grade', 'D']}, 'then': 4.0},
                                        {'case': {'$eq': ['$$enrollment.grade', 'F']}, 'then': 5.0}
                                    ],
                                    'default': None
                                }
                            }
                        }
                    }
                }
            }
        }
    ]
    
    students = list(students_collection.aggregate(pipeline))
    
    for student in students:
        student_table.insert("", "end", values=(
            str(student['_id']),
            student['first_name'],
            student['last_name'],
            student['email'],
            student.get('date_of_birth', ''),
            student['major'],
            student['total_courses'],
            round(student['gwa'], 2) if student['gwa'] is not None else 'N/A'
        ))

def load_courses():
    for row in course_table.get_children():
        course_table.delete(row)
    
    pipeline = [
        {
            '$lookup': {
                'from': 'enrollments',
                'localField': 'course_id',
                'foreignField': 'course_id',
                'as': 'enrollments'
            }
        },
        {
            '$addFields': {
                'enrolled_students': {'$size': '$enrollments'},
                'avg_course_grade': {
                    '$avg': {
                        '$map': {
                            'input': '$enrollments',
                            'as': 'enrollment',
                            'in': {
                                '$switch': {
                                    'branches': [
                                        {'case': {'$eq': ['$$enrollment.grade', 'A']}, 'then': 1.0},
                                        {'case': {'$eq': ['$$enrollment.grade', 'B']}, 'then': 2.0},
                                        {'case': {'$eq': ['$$enrollment.grade', 'C']}, 'then': 3.0},
                                        {'case': {'$eq': ['$$enrollment.grade', 'D']}, 'then': 4.0},
                                        {'case': {'$eq': ['$$enrollment.grade', 'F']}, 'then': 5.0}
                                    ],
                                    'default': None
                                }
                            }
                        }
                    }
                }
            }
        }
    ]
    
    courses = list(courses_collection.aggregate(pipeline))
    
    for course in courses:
        course_table.insert("", "end", values=(
            course['course_id'],
            course['course_name'],
            course['department'],
            course['credits'],
            course['instructor'],
            course['enrolled_students'],
            round(course['avg_course_grade'], 2) if course['avg_course_grade'] is not None else 'N/A'
        ))

def load_enrollments():
    for row in enrollment_table.get_children():
        enrollment_table.delete(row)
    pipeline = [
        {
            '$lookup': {
                'from': 'students',
                'localField': 'student_id',
                'foreignField': '_id',
                'as': 'student'
            }
        },
        {
            '$lookup': {
                'from': 'courses',
                'localField': 'course_id',
                'foreignField': 'course_id',
                'as': 'course'
            }
        },
        {
            '$unwind': '$student'
        },
        {
            '$unwind': '$course'
        }
    ]
    
    enrollments = list(enrollments_collection.aggregate(pipeline))
    
    for enrollment in enrollments:
        enrollment_table.insert("", "end", values=(
            str(enrollment['_id']),
            str(enrollment['student_id']),
            enrollment['course_id'],
            enrollment['semester'],
            enrollment['enrollment_date'],
            enrollment['grade'],
            f"{enrollment['student']['first_name']} {enrollment['student']['last_name']}",
            enrollment['course']['course_name']
        ))

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

students_frame = ttk.Frame(notebook)
notebook.add(students_frame, text="Students")

student_columns = ("ID", "First Name", "Last Name", "Email", "Date of Birth", "Major", "Total Courses", "GWA")
student_table = ttk.Treeview(students_frame, columns=student_columns, show="headings", height=10)

for col in student_columns:
    student_table.heading(col, text=col)
    student_table.column(col, anchor='center', width=100)

student_table.pack(fill="both", expand=True, padx=20, pady=10)

student_input_frame = tk.Frame(students_frame, bg="#e8f1f5")
student_input_frame.pack(pady=10)

student_fields = [
    ("First Name:", "first_name"),
    ("Last Name:", "last_name"),
    ("Email:", "email"),
    ("Date of Birth:", "dob"),
    ("Major:", "major")
]

for i, (label_text, entry_name) in enumerate(student_fields):
    row = i // 2
    col = (i % 2) * 2
    
    tk.Label(student_input_frame, text=label_text, bg="#e8f1f5").grid(row=row, column=col, padx=5, pady=5, sticky='w')
    globals()[entry_name] = ttk.Entry(student_input_frame, width=20)
    globals()[entry_name].grid(row=row, column=col+1, padx=5, pady=5)

student_buttons_frame = tk.Frame(students_frame, bg="#e8f1f5")
student_buttons_frame.pack(pady=10)

ttk.Button(student_buttons_frame, text="Add Student", command=add_student).grid(row=0, column=0, padx=5)
ttk.Button(student_buttons_frame, text="Update Student", command=update_student).grid(row=0, column=1, padx=5)
ttk.Button(student_buttons_frame, text="Delete Student", command=delete_student).grid(row=0, column=2, padx=5)
ttk.Button(student_buttons_frame, text="Clear Fields", command=clear_fields).grid(row=0, column=3, padx=5)

courses_frame = ttk.Frame(notebook)
notebook.add(courses_frame, text="Courses")

course_columns = ("Course ID", "Course Name", "Department", "Credits", "Instructor", "Enrolled Students", "Course Grade")
course_table = ttk.Treeview(courses_frame, columns=course_columns, show="headings", height=10)

for col in course_columns:
    course_table.heading(col, text=col)
    course_table.column(col, anchor='center', width=100)

course_table.pack(fill="both", expand=True, padx=20, pady=10)

course_input_frame = tk.Frame(courses_frame, bg="#e8f1f5")
course_input_frame.pack(pady=10)

course_fields = [
    ("Course ID:", "course_id"),
    ("Course Name:", "course_name"),
    ("Department:", "department"),
    ("Credits:", "credits"),
    ("Instructor:", "instructor")
]

for i, (label_text, entry_name) in enumerate(course_fields):
    row = i // 2
    col = (i % 2) * 2
    
    tk.Label(course_input_frame, text=label_text, bg="#e8f1f5").grid(row=row, column=col, padx=5, pady=5, sticky='w')
    globals()[entry_name] = ttk.Entry(course_input_frame, width=20)
    globals()[entry_name].grid(row=row, column=col+1, padx=5, pady=5)

course_buttons_frame = tk.Frame(courses_frame, bg="#e8f1f5")
course_buttons_frame.pack(pady=10)

ttk.Button(course_buttons_frame, text="Add Course", command=add_course).grid(row=0, column=0, padx=5)
ttk.Button(course_buttons_frame, text="Update Course", command=update_course).grid(row=0, column=1, padx=5)
ttk.Button(course_buttons_frame, text="Delete Course", command=delete_course).grid(row=0, column=2, padx=5)
ttk.Button(course_buttons_frame, text="Clear Fields", command=clear_fields).grid(row=0, column=3, padx=5)

enrollments_frame = ttk.Frame(notebook)
notebook.add(enrollments_frame, text="Enrollments")

enrollment_columns = ("Enrollment ID", "Student ID", "Course ID", "Semester", "Enrollment Date", "Grade", "Student Name", "Course Name")
enrollment_table = ttk.Treeview(enrollments_frame, columns=enrollment_columns, show="headings", height=10)

for col in enrollment_columns:
    enrollment_table.heading(col, text=col)
    enrollment_table.column(col, anchor='center', width=100)
enrollment_table.pack(fill="both", expand=True, padx=20, pady=10)
enrollment_input_frame = tk.Frame(enrollments_frame, bg="#e8f1f5")
enrollment_input_frame.pack(pady=10)

tk.Label(enrollment_input_frame, text="Semester:", bg="#e8f1f5").grid(row=0, column=0, padx=5, pady=5, sticky='w')
semester = ttk.Entry(enrollment_input_frame, width=20)
semester.grid(row=0, column=1, padx=5, pady=5)

enrollment_buttons_frame = tk.Frame(enrollments_frame, bg="#e8f1f5")
enrollment_buttons_frame.pack(pady=10)

ttk.Button(enrollment_buttons_frame, text="Add Enrollment", command=add_enrollment).grid(row=0, column=0, padx=5)
ttk.Button(enrollment_buttons_frame, text="Update Enrollment", command=update_enrollment).grid(row=0, column=1, padx=5)
ttk.Button(enrollment_buttons_frame, text="Delete Enrollment", command=delete_enrollment).grid(row=0, column=2, padx=5)
ttk.Button(enrollment_buttons_frame, text="Clear Fields", command=clear_fields).grid(row=0, column=3, padx=5)

def on_closing():
    if db.is_connected():
        cursor.close()
        db.close()
    root.destroy()

load_students()
load_courses()
load_enrollments()

root.mainloop()