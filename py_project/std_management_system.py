#Student management system
#1.add students
#2.display students
#3.update student marks
#4.update student age
#5.update attendance
#6.search student
#7.remove students
#8.add new subject
#9.exit

import csv
import os
#stores information of single student
class Student:
    def __init__(self, std_id, name, age, course, subjects, attendance):
        self.std_id = std_id
        self.name = name
        self.age = age
        self.course = course
        self.subjects = subjects
        self.attendance = float(attendance)

    def display(self):
        total = sum(self.subjects.values())
        average = total / len(self.subjects)

        if average >= 90:
            grade = "A+"
        elif average >= 80:
            grade = "A"
        elif average >= 70:
            grade = "B+"
        elif average >= 60:
            grade = "B"
        elif average >= 50:
            grade = "C"
        elif average >= 40:
            grade = "D"
        else:
            grade = "Fail"

        low_subject = min(self.subjects, key=self.subjects.get)

        if average >= 75 and self.attendance >= 75:
            performance = "Excellent"
        elif average >= 60 and self.attendance >= 75:
            performance = "Good"
        elif average >= 50 and self.attendance >= 65:
            performance = "Average"
        else:
            performance = "Needs Improvement"

        print("\nID:", self.std_id)
        print("Name:", self.name)
        print("Age:", self.age)
        print("Course:", self.course)

        for subject, marks in self.subjects.items():
            print(f"{subject}: {marks}")

        print("Total Marks:", total)
        print(f"Average: {average:.2f}")
        print("Grade:", grade)
        print("Attendance:", self.attendance, "%")
        print("Performance:", performance)

        if self.subjects[low_subject] < 80:
            print("Disclaimer: Need to improve in", low_subject)
        else:
            print("Disclaimer: Keep maintaining your performance")

        if self.attendance < 75:
            print("Note: Attendance needs improvement")

        print("-" * 30)

#stores all students 
class StudentManagement:
    def __init__(self):
        self.file = "students.csv"
        self.subjects = ["Python", "Java", "DBMS"]
        self.students = []
        self.load_students()

    # Load data from CSV
    def load_students(self):
        if not os.path.exists(self.file):
            return

        with open(self.file, "r", newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:
                subjects = {
                    subject: float(row[subject])
                    for subject in self.subjects
                    if subject in row
                }

                student = Student(
                    row["ID"],
                    row["Name"],
                    row["Age"],
                    row["Course"],
                    subjects,
                    row["Attendance"]
                )
                self.students.append(student)

    # Save data to CSV
    def save_students(self):
        fields = ["ID", "Name", "Age", "Course"] + self.subjects + ["Attendance"]

        with open(self.file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()

            for student in self.students:
                row = {
                    "ID": student.std_id,
                    "Name": student.name,
                    "Age": student.age,
                    "Course": student.course,
                    "Attendance": student.attendance
                }

                for subject in self.subjects:
                    row[subject] = student.subjects.get(subject, 0)
                writer.writerow(row)

    # Add student
    def add_student(self):
        std_id = input("Enter student ID: ")

        for student in self.students:
            if std_id == student.std_id:
                print("Student ID already exists")
                return

        name = input("Enter student name: ")
        age = int(input("Enter student age: "))
        course = input("Enter student course: ")

        subjects = {}

        for subject in self.subjects:
            subjects[subject] = float(input(f"Enter {subject} marks: "))
        attendance = float(input("Enter attendance percentage: "))

        student = Student(std_id, name, age, course, subjects, attendance)
        self.students.append(student)
        self.save_students()

        print("Student added successfully!!")

    # Display students
    def display_student(self):
        if not self.students:
            print("No students available")
            return
        print("\n------ Students List ------")
        for i, student in enumerate(self.students, 1):
            print(f"{i}. {student.std_id} - {student.name}")
        choice = int(input("\nEnter student number to view details: "))
        if 1 <= choice <= len(self.students):
            self.students[choice - 1].display()
        else:
            print("Invalid student number")
    # Update marks
    def update_studentmarks(self):
        std_id = input("Enter student ID: ")
        for student in self.students:
            if student.std_id == std_id:
                print("\nSubjects:", ", ".join(student.subjects.keys()))

                subject = input("Enter subject name to update: ")

                if subject in student.subjects:
                    student.subjects[subject] = float(input(f"Enter new {subject} marks: "))
                    self.save_students()
                    print("Marks updated successfully!!")
                else:
                    print("Subject not found")
                return

        print("Student not found")

    # Update age
    def update_studentage(self):
        std_id = input("Enter student ID: ")

        for student in self.students:
            if student.std_id == std_id:
                student.age = int(input("Enter new age: "))
                self.save_students()
                print("Age updated successfully!!")
                return
        print("Student not found")

    # Update attendance
    def update_attendance(self):
        std_id = input("Enter student ID: ")
        for student in self.students:
            if student.std_id == std_id:
                student.attendance = float(input("Enter new attendance: "))
                self.save_students()
                print("Attendance updated successfully!!")
                return
        print("Student not found")

    # Search student
    def search_student(self):
        std_id = input("Enter student ID: ")
        for student in self.students:
            if student.std_id == std_id:
                student.display()
                return
        print("Student not found")

    # Remove student
    def remove_student(self):
        std_id = input("Enter student ID: ")
        for student in self.students:
            if student.std_id == std_id:
                confirm = input("Enter y to confirm delete: ")
                if confirm.lower() == "y":
                    self.students.remove(student)
                    self.save_students()
                    print("Student removed successfully!!")
                else:
                    print("Remove cancelled")
                return
        print("Student not found")

    # Add new subject
    def add_subject(self):
        subject = input("Enter new subject name: ")
        if subject in self.subjects:
            print("Subject already exists")
            return
        self.subjects.append(subject)
        for student in self.students:
            student.subjects[subject] = 0
        self.save_students()
        print("Subject added successfully!!")

# Main program
student_management = StudentManagement()

while True:

    print("\n------ Student Management System ------")
    print("1. ADD STUDENT")
    print("2. DISPLAY STUDENTS")
    print("3. UPDATE STUDENT MARKS")
    print("4. UPDATE STUDENT AGE")
    print("5. UPDATE ATTENDANCE")
    print("6. SEARCH STUDENT")
    print("7. REMOVE STUDENT")
    print("8. ADD NEW SUBJECT")
    print("9. EXIT")

    choice = input("Enter your choice: ")

    if choice == "1":
        student_management.add_student()

    elif choice == "2":
        student_management.display_student()

    elif choice == "3":
        student_management.update_studentmarks()

    elif choice == "4":
        student_management.update_studentage()

    elif choice == "5":
        student_management.update_attendance()

    elif choice == "6":
        student_management.search_student()

    elif choice == "7":
        student_management.remove_student()

    elif choice == "8":
        student_management.add_subject()

    elif choice == "9":
        print("Thank You!!")
        break

    else:
        print("Invalid choice")