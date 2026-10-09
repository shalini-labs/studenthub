
import sqlite3


DATABASE_NAME = "studenthub.db"


def create_database():
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_number TEXT UNIQUE NOT NULL,
            student_class TEXT NOT NULL,
            email TEXT
        )
    """)

    connection.commit()
    connection.close()


def add_student(name, roll_number, student_class, email):
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO students
        (name, roll_number, student_class, email)
        VALUES (?, ?, ?, ?)
    """, (name, roll_number, student_class, email))

    connection.commit()
    connection.close()


def get_students():
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, roll_number, student_class, email
        FROM students
        ORDER BY id DESC
    """)

    students = cursor.fetchall()

    connection.close()

    return students


if __name__ == "__main__":
    create_database()
    print("StudentHub database is ready!")