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
    print("--- Insert Student Details ---\n")
    id = input("Enter ID: ")
    i = input("Enter Student ID: ")
    n = input("Enter Student Name: ")
    d = input("Enter Student DOB: ")
    dep = input("Enter Student Department: ")
    ph = input("Enter Student Phone No: \n")

    c.execute("""
    INSERT INTO Students_details(ID, STUDENT_ID, NAME, DOB, DEPARTMENT, PHONE_No)
    VALUES (?,?,?,?,?,?)
    """, (id, i, n, d, dep, ph))

    conn.commit()
    print("Student details inserted successfully!\n")


def insert_academic_details():
    print("--- Insert Academic Details ---\n")
    en = int(input("English mark: "))
    gen = int(input("Genetics mark: "))
    mi = int(input("Microbiology mark: "))
    data = int(input("Data mining mark: "))
    stati = int(input("Statistics mark: "))
    attend = float(input("Attendance percentage: "))
    st_id = input("Student ID:")

    c.execute("""
    INSERT INTO Academic_details(English, Genetics, Microbiology, Data_mining, Statistics, Attendance_Percentage, Student_id)
    VALUES (?,?,?,?,?,?,?)
    """, (en, gen, mi, data, stati, attend, st_id))

    conn.commit()
    print("Academic details inserted successfully!\n")

# UPDATE FUNCTIONS

def update_phone():
    print("---- Update Phone Number ----\n")
    st_id = input("Enter your Student ID: ")
    new_phone = input("Enter new phone number: ")
    c.execute("UPDATE Students_details SET PHONE_No = ? WHERE Student_id = ?", (new_phone, st_id))
    conn.commit()
    print("Phone number updated successfully!\n")

def update_attendance():
    print("---- Update Attendance Details ----\n")
    st_id = int(input("Student ID: "))
    new_attendance = input("New Attendance percentage: ")
    c.execute("UPDATE Academic_details SET Attendance_Percentage = ? WHERE Student_id = ?", (new_attendance, st_id) )
    if c.rowcount == 0:
        print("No student found with this Student ID.\n")
    else:
        print("Attendance updated successfully!\n")
        conn.commit()

def update_marks():
    print("---- Update Examination Results ----\n")
    st_id = int(input("Enter your Student ID: "))
    subject = input("Enter subject name (English/Genetics/Microbiology/Data/Statistics): ")
    new_mark = int(input("Enter the new marks: "))
    query = f"UPDATE Academic_details SET {subject} = ? WHERE Student_id = ?"
    c.execute(query, (new_mark, st_id))
    conn.commit()

    print("Marks updated successfully!\n")
    

# VIEW FUNCTIONS

def view_student_details():
    print("--- Student Details ---\n")
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
    print("--- Academic Result ---\n")
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
    print("--- Attendance Percentage ---\n")
    st_id = input("Enter Student ID: ")
    c.execute(""" SELECT Attendance_Percentage FROM Academic_details WHERE Student_id=? """, (st_id,))
    result = c.fetchone()

    if result:
        print("Attendance Percentage:", result[0])


def view_students_details():
    print("=============Student Details==============\n")
    c.execute("SELECT * FROM Students_details")
    result = c.fetchall()
    if result:
      for row in result:
         print(row)


def view_academics_result():
    print("==========Academic Details==========\n")
    c.execute("SELECT * FROM Academic_details")
    result = c.fetchall()
    if result:
        for row in result:
            print(row)


# AUTHENTICATION

def register():
    print("====== REGISTRATION ======\n")
    U = input("Enter username: ")
    P = input("Enter password: ")
    P1 = input("Confirm password: ")
    T = input("Enter user type (Student/Teacher): ")

    if P == P1:
        c.execute(""" INSERT INTO Academic (Username,Password,User_Type)
       VALUES(?,?,?);
       """, (U, P, T))
        print("Registered successfully!")
        conn.commit()
    else:
        print("Invalid, please check your password")


def login():
    print("===== LOGIN PAGE =====\n")
    Us = input("Username: ")
    Pw = input("Password: ")
    Ty = input("User type (Student/Teacher): ")

    c.execute("SELECT * FROM Academic WHERE Username=? AND Password=? AND User_Type=?",
              (Us, Pw, Ty))
    result = c.fetchone()

    if not result:
        print("Invalid login!")
        return

    print("Login successful! Welcome", Us,"\n")

    if Ty == "Student":
        while True:
            
            print("1. View Student details")
            print("2. View Academic Results")
            print("3. view attendance percentage")
            print("4. Update phone number")
            print("5. Logout")

            ch = input("Enter your choice: ")
            if ch == "1":
                view_student_details()
            elif ch == "2":
                view_academic_result()
            elif ch == "3":
                view_attendance_percentage()
            elif ch== "4":
                update_phone()
            elif ch == "5":
                break

    else:  # Teacher
        while True:
            print("1. Insert Student Details")
            print("2. Insert Academic Details")
            print("3. update attendance percentage")
            print("4. Update Examination Result")
            print("5. View Students Details")
            print("6. View Academics Results")
            print("7. Logout")

            ch = input("Enter your choice: ")

            if ch == "1":
                insert_details()
            elif ch == "2":
                insert_academic_details()
            elif ch == "3":
                update_attendance()
            elif ch == "4":
                update_marks()
            elif ch == "5":
                view_students_details()
            elif ch == "6":
                view_academics_result()
            elif ch == "7":
                break

# HOME PAGE

while True:
    print("====== STUDENT GRADING SYSTEM ======\n")

    print("1. Registration")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter your choice (1/2/3): ")

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