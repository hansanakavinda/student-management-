import sqlite3
import hashlib
import os

class Database:
    def __init__(self, db_name="app_database.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Connect to the database"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            
    def hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def initialize_database(self):
        """Create tables and seed initial data"""
        self.connect()
        
        # Create users table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create students table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                date_of_birth DATE NOT NULL,
                gender TEXT NOT NULL,
                address TEXT NOT NULL,
                guardian_name TEXT NOT NULL,
                guardian_nic TEXT NOT NULL,
                guardian_contact TEXT NOT NULL,
                image_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create exam_results table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS exam_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                subject TEXT NOT NULL,
                exam_name TEXT NOT NULL,
                exam_date DATE NOT NULL,
                marks_obtained REAL NOT NULL,
                total_marks REAL NOT NULL,
                grade TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students (id)
            )
        ''')
        
        # Check if admin user exists
        self.cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        if not self.cursor.fetchone():
            # Seed admin user with password '1234'
            hashed_password = self.hash_password('1234')
            self.cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                ('admin', hashed_password)
            )
            self.conn.commit()
            print("Admin user created successfully!")
        
        self.close()
        
    def authenticate_user(self, username, password):
        """Authenticate user credentials"""
        self.connect()
        hashed_password = self.hash_password(password)
        
        self.cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, hashed_password)
        )
        
        user = self.cursor.fetchone()
        self.close()
        
        return user is not None
    
    def add_student(self, student_data):
        """Add a new student to the database"""
        self.connect()
        try:
            self.cursor.execute(
                '''INSERT INTO students 
                   (student_name, date_of_birth, gender, address, 
                    guardian_name, guardian_nic, guardian_contact, image_path) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                student_data
            )
            self.conn.commit()
            student_id = self.cursor.lastrowid
            self.close()
            return True, student_id
        except Exception as e:
            self.close()
            return False, str(e)
    
    def get_all_students(self):
        """Retrieve all students from database"""
        self.connect()
        self.cursor.execute("SELECT * FROM students ORDER BY student_name")
        students = self.cursor.fetchall()
        self.close()
        return students
    
    def get_student_by_id(self, student_id):
        """Get student details by ID"""
        self.connect()
        self.cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        student = self.cursor.fetchone()
        self.close()
        return student
    
    def add_exam_result(self, result_data):
        """Add exam result for a student"""
        self.connect()
        try:
            self.cursor.execute(
                '''INSERT INTO exam_results 
                   (student_id, subject, exam_name, exam_date, marks_obtained, total_marks, grade) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)''',
                result_data
            )
            self.conn.commit()
            self.close()
            return True, "Result added successfully"
        except Exception as e:
            self.close()
            return False, str(e)
    
    def get_student_results(self, student_id):
        """Get all exam results for a student"""
        self.connect()
        self.cursor.execute(
            "SELECT * FROM exam_results WHERE student_id = ? ORDER BY exam_date DESC",
            (student_id,)
        )
        results = self.cursor.fetchall()
        self.close()
        return results
    
    def search_students(self, search_term):
        """Search students by name"""
        self.connect()
        self.cursor.execute(
            "SELECT * FROM students WHERE student_name LIKE ? ORDER BY student_name",
            (f"%{search_term}%",)
        )
        students = self.cursor.fetchall()
        self.close()
        return students
    
    def update_student(self, student_id, student_data):
        """Update student information"""
        self.connect()
        try:
            self.cursor.execute(
                '''UPDATE students 
                   SET student_name=?, date_of_birth=?, gender=?, address=?, 
                       guardian_name=?, guardian_nic=?, guardian_contact=?, image_path=?
                   WHERE id=?''',
                (*student_data, student_id)
            )
            self.conn.commit()
            self.close()
            return True, "Student updated successfully"
        except Exception as e:
            self.close()
            return False, str(e)
    
    def delete_student(self, student_id):
        """Delete student and their exam results"""
        self.connect()
        try:
            # Delete exam results first (foreign key constraint)
            self.cursor.execute("DELETE FROM exam_results WHERE student_id = ?", (student_id,))
            # Delete student
            self.cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
            self.conn.commit()
            self.close()
            return True, "Student deleted successfully"
        except Exception as e:
            self.close()
            return False, str(e)
    
    def get_all_exam_results(self, student_name=None, exam_name=None, exam_date=None):
        """Get all exam results with optional filters"""
        self.connect()
        
        query = '''SELECT 
                    exam_results.id,
                    students.id as student_id,
                    students.student_name,
                    exam_results.subject,
                    exam_results.exam_name,
                    exam_results.exam_date,
                    exam_results.marks_obtained,
                    exam_results.total_marks,
                    exam_results.grade
                   FROM exam_results
                   JOIN students ON exam_results.student_id = students.id
                   WHERE 1=1'''
        
        params = []
        
        if student_name:
            query += " AND students.student_name LIKE ?"
            params.append(f"%{student_name}%")
        
        if exam_name:
            query += " AND exam_results.exam_name LIKE ?"
            params.append(f"%{exam_name}%")
        
        if exam_date:
            query += " AND exam_results.exam_date = ?"
            params.append(exam_date)
        
        query += " ORDER BY exam_results.exam_date DESC, students.student_name"
        
        self.cursor.execute(query, params)
        results = self.cursor.fetchall()
        self.close()
        return results
