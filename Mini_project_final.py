# STUDENT GRADING SYSTEM

import sqlite3

conn = sqlite3.connect("Gradingss.db")
c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON")

# TABLES

c.execute("""
CREATE TABLE IF NOT EXISTS Academic (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT,
    Password TEXT UNIQUE,
    User_Type TEXT
);
""")

# c.execute(""" CREATE TABLE IF NOT EXISTS Student_details(       #DROP THE TABLE Student_details
# ID INTEGER PRIMARY KEY AUTOINCREMENT,
# STUDENT_ID INTEGER,
# NAME Text,
# DOB Text,
# Department Text,
# PHONE_No INT);
# """)
# c.execute("ALTER TABLE Student_details RENAME COLUMN Department to DEPARTMENT")
#
# c.execute("DROP TABLE IF EXISTS Student_details")

c.execute("""
CREATE TABLE IF NOT EXISTS Students_details(
    ID INTEGER,
    STUDENT_ID INTEGER PRIMARY KEY,
    NAME TEXT,
    DOB TEXT,
    DEPARTMENT TEXT,
    PHONE_No INT
);
""")

c.execute("""
CREATE TABLE IF NOT EXISTS Academic_details(
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    English INTEGER,
    Genetics INTEGER,
    Microbiology INTEGER,
    Data_mining INTEGER,
    Statistics INTEGER,
    Attendance_Percentage REAL,
    Student_id INTEGER,
    FOREIGN KEY(Student_id) REFERENCES Students_details(STUDENT_ID)
);
""")

# INSERT FUNCTIONS

def insert_details():
    print("--- Insert Student Details ---")
    id = input("Enter ID: ")
    i = input("Enter Student ID: ")
    n = input("Enter Student Name: ")
    d = input("Enter Student DOB: ")
    dep = input("Enter Student Department: ")
    ph = input("Enter Student Phone No: ")

    c.execute("""
    INSERT INTO Students_details(ID, STUDENT_ID, NAME, DOB, DEPARTMENT, PHONE_No)
    VALUES (?,?,?,?,?,?)
    """, (id, i, n, d, dep, ph))

    conn.commit()
    print("Student details inserted successfully!")


def insert_academic_details():
    print("--- Insert Academic Details ---")
    en = int(input("English mark: "))
    gen = int(input("Genetics mark: "))
    mi = int(input("Microbiology mark: "))
    data = int(input("Data mining mark: "))
    stati = int(input("Statistics mark: "))
    attend = float(input("Attendance percentage: "))
    st_id = input("Student ID: ")

    c.execute("""
    INSERT INTO Academic_details(English, Genetics, Microbiology, Data_mining, Statistics, Attendance_Percentage, Student_id)
    VALUES (?,?,?,?,?,?,?)
    """, (en, gen, mi, data, stati, attend, st_id))

    conn.commit()
    print("Academic details inserted successfully")

# UPDATE FUNCTION

def update_attendance():
    print("--- Update Attendance Details ---")
    st_id = int(input("Student ID: "))
    new_attendance = input("New Attendance percentage: ")
    c.execute("UPDATE Academic_details SET Attendance_Percentage = ? WHERE Student_id = ?", (new_attendance, st_id) )
    if c.rowcount == 0:
        print("No student found with this Student ID.")
    else:
        conn.commit()
        print("Attendance updated successfully!")

# VIEW FUNCTIONS

def view_student_details():
    print("--- Student Details ---")
    st_id = input("Enter Student ID: ")

    c.execute("SELECT * FROM Students_details WHERE STUDENT_ID=?", (st_id,))
    result = c.fetchone()

    if result:
        print("ID:", result[0])
        print("Student ID:", result[1])
        print("Name:", result[2])
        print("DOB:", result[3])
        print("Department:", result[4])
        print("Phone No:", result[5])
    else:
        print("No student found.")


def view_academic_result():
    print("--- Academic Result ---")
    st_id = input("Enter Student ID: ")

    c.execute("""
        SELECT English, Genetics, Microbiology, Data_mining, Statistics, Attendance_Percentage
        FROM Academic_details WHERE Student_id=?
    """, (st_id,))
    result = c.fetchone()

    if result:
        total = sum(result[:5])
        percentage = total / 5
        if percentage >= 90:
            grade = "A+"
        elif percentage >= 80:
            grade = "A"
        elif percentage >= 70:
            grade = "B"
        elif percentage >= 60:
            grade = "C"
        else:
            grade = "D"

        print("Marks:", result[:5])
        print("Total:", total)
        print("Percentage:", percentage)
        print("Grade:", grade)
    else:
        print("No academic details found.")


def view_attendance_percentage():
    print("--- Attendance Percentage ---")
    st_id = input("Enter Student ID: ")
    c.execute(""" SELECT Attendance_Percentage FROM Academic_details WHERE Student_id=? """, (st_id,))
    result = c.fetchone()

    if result:
        print("Attendance Percentage:", result[0])

# AUTHENTICATION

def register():
    print("--- REGISTRATION ---")
    U = input("Enter username: ")
    P = input("Enter password: ")
    P1 = input("Confirm password: ")
    T = input("Enter user type (Student/Teacher): ")

    if P == P1:
        c.execute(""" INSERT INTO Academic (Username,Password,User_Type)
       VALUES(?,?,?);
       """, (U, P, T))
        print("Registered successfully!")
    else:
        print("Invalid, please check your password")


def login():
    print("--- LOGIN PAGE ---")
    Us = input("Username: ")
    Pw = input("Password: ")
    Ty = input("User type (Student/Teacher): ")

    c.execute("SELECT * FROM Academic WHERE Username=? AND Password=? AND User_Type=?",
              (Us, Pw, Ty))
    result = c.fetchone()

    if not result:
        print("Invalid login!")
        return

    print("Login successful. Welcome", Us)

    if Ty == "Student":
        while True:
            print("1. View Student details")
            print("2. View Academic Results")
            print("3. view attendance percentage")
            print("4. Logout")

            ch = input("Enter choice: ")
            if ch == "1":
                view_student_details()
            elif ch == "2":
                view_academic_result()
            elif ch == "3":
                view_attendance_percentage()
            elif ch == "4":
                break

    else:                                               # Teacher
        while True:
            print("1. Insert Student Details")
            print("2. Insert Academic Details")
            print("3. update attendance percentage")
            print("4. View Student Details")
            print("5. View Academic Results")
            print("6. Logout")

            ch = input("Enter choice: ")

            if ch == "1":
                insert_details()
            elif ch == "2":
                insert_academic_details()
            elif ch == "3":
                update_attendance()
            elif ch == "4":
                view_student_details()
            elif ch == "5":
                view_academic_result()
            elif ch == "6":
                break

# HOME PAGE

while True:
    print("====== STUDENT GRADING SYSTEM ======")
    print("1. Registration")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        register()
    elif choice == "2":
        login()
    elif choice == "3":
        print("Thank you!")
        break
    else:
        print("Invalid choice. Try again.")

conn.commit()