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
                registration_date DATE,
                grade TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create exam_results table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS exam_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                exam_name TEXT NOT NULL,
                exam_year INTEGER NOT NULL,
                marks_obtained REAL NOT NULL,
                grade TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students (id)
            )
        ''')
        
        # Create student_notes table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS student_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER UNIQUE NOT NULL,
                notes TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students (id)
            )
        ''')
        
        # Create certificates table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS certificates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                certificate_image_path TEXT NOT NULL,
                note TEXT,
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
    
    def add_student(self, student_data, certificates_data=None):
        """Add a new student to the database with optional certificates"""
        self.connect()
        try:
            self.cursor.execute(
                '''INSERT INTO students 
                   (student_name, date_of_birth, gender, address, 
                    guardian_name, guardian_nic, guardian_contact, image_path,
                    registration_date, grade) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                student_data
            )
            self.conn.commit()
            student_id = self.cursor.lastrowid
            
            # Add certificates if provided
            if certificates_data:
                for cert_path, cert_note in certificates_data:
                    self.cursor.execute(
                        '''INSERT INTO certificates 
                           (student_id, certificate_image_path, note) 
                           VALUES (?, ?, ?)''',
                        (student_id, cert_path, cert_note)
                    )
                self.conn.commit()
            
            self.close()
            return True, student_id
        except Exception as e:
            self.close()
            return False, str(e)
    
    def get_all_students(self):
        """Retrieve all students from database"""
        self.connect()
        self.cursor.execute("SELECT * FROM students ORDER BY id")
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
                   (student_id, exam_name, exam_year, marks_obtained, grade) 
                   VALUES (?, ?, ?, ?, ?)''',
                result_data
            )
            self.conn.commit()
            self.close()
            return True, "Result added successfully"
        except Exception as e:
            self.close()
            return False, str(e)
    
    def update_exam_result(self, result_id, result_data):
        """Update exam result"""
        self.connect()
        try:
            self.cursor.execute(
                '''UPDATE exam_results 
                   SET student_id=?, exam_name=?, exam_year=?, marks_obtained=?, grade=?
                   WHERE id=?''',
                (*result_data, result_id)
            )
            self.conn.commit()
            self.close()
            return True, "Result updated successfully"
        except Exception as e:
            self.close()
            return False, str(e)
    
    def delete_exam_result(self, result_id):
        """Delete exam result"""
        self.connect()
        try:
            self.cursor.execute("DELETE FROM exam_results WHERE id = ?", (result_id,))
            self.conn.commit()
            self.close()
            return True, "Result deleted successfully"
        except Exception as e:
            self.close()
            return False, str(e)
    
    def get_exam_result_by_id(self, result_id):
        """Get a specific exam result by ID"""
        self.connect()
        self.cursor.execute(
            '''SELECT 
                exam_results.id,
                students.id as student_id,
                students.student_name,
                exam_results.exam_name,
                exam_results.exam_year,
                exam_results.marks_obtained,
                exam_results.grade
               FROM exam_results
               JOIN students ON exam_results.student_id = students.id
               WHERE exam_results.id = ?''',
            (result_id,)
        )
        result = self.cursor.fetchone()
        self.close()
        return result
    
    def get_student_results(self, student_id):
        """Get all exam results for a student"""
        self.connect()
        self.cursor.execute(
            "SELECT * FROM exam_results WHERE student_id = ? ORDER BY exam_year DESC, exam_name",
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
                   guardian_name = ?, guardian_nic = ?, guardian_contact = ?, image_path = ?,
                   registration_date = ?, grade = ?
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
    
    def get_all_exam_results(self, student_name=None, exam_name=None, exam_year=None):
        """Get all exam results with optional filters"""
        self.connect()
        
        query = '''SELECT 
                    exam_results.id,
                    students.id as student_id,
                    students.student_name,
                    exam_results.exam_name,
                    exam_results.exam_year,
                    exam_results.marks_obtained,
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
        
        if exam_year:
            query += " AND exam_results.exam_year = ?"
            params.append(exam_year)
        
        query += " ORDER BY exam_results.exam_year DESC, students.student_name"
        
        self.cursor.execute(query, params)
        results = self.cursor.fetchall()
        self.close()
        return results
    
    def get_student_notes(self, student_id):
        """Get notes for a specific student"""
        self.connect()
        self.cursor.execute(
            "SELECT notes FROM student_notes WHERE student_id = ?",
            (student_id,)
        )
        result = self.cursor.fetchone()
        self.close()
        return result[0] if result else ""
    
    def save_student_notes(self, student_id, notes):
        """Save or update notes for a student"""
        self.connect()
        try:
            # Check if notes exist
            self.cursor.execute(
                "SELECT id FROM student_notes WHERE student_id = ?",
                (student_id,)
            )
            existing = self.cursor.fetchone()
            
            if existing:
                # Update existing notes
                self.cursor.execute(
                    '''UPDATE student_notes 
                       SET notes = ?, updated_at = CURRENT_TIMESTAMP 
                       WHERE student_id = ?''',
                    (notes, student_id)
                )
            else:
                # Insert new notes
                self.cursor.execute(
                    '''INSERT INTO student_notes (student_id, notes) 
                       VALUES (?, ?)''',
                    (student_id, notes)
                )
            
            self.conn.commit()
            self.close()
            return True, "Notes saved successfully"
        except Exception as e:
            self.close()
            return False, str(e)
    
    def add_certificate(self, student_id, certificate_image_path, note=""):
        """Add a new certificate for a student"""
        try:
            self.connect()
            self.cursor.execute(
                """INSERT INTO certificates (student_id, certificate_image_path, note) 
                   VALUES (?, ?, ?)""",
                (student_id, certificate_image_path, note)
            )
            self.conn.commit()
            return True, "Certificate added successfully"
        except Exception as e:
            return False, str(e)
        finally:
            self.close()
    
    def get_certificates_by_student(self, student_id):
        """Get all certificates for a specific student"""
        try:
            self.connect()
            self.cursor.execute(
                """SELECT c.id, c.student_id, c.certificate_image_path, c.note, c.created_at,
                          s.student_name
                   FROM certificates c
                   JOIN students s ON c.student_id = s.id
                   WHERE c.student_id = ?
                   ORDER BY c.created_at DESC""",
                (student_id,)
            )
            return self.cursor.fetchall()
        finally:
            self.close()
    
    def get_all_certificates(self, student_name_filter=""):
        """Get all certificates with optional student name filter"""
        try:
            self.connect()
            
            if student_name_filter:
                self.cursor.execute(
                    """SELECT c.id, c.student_id, c.certificate_image_path, c.note, c.created_at,
                              s.student_name
                       FROM certificates c
                       JOIN students s ON c.student_id = s.id
                       WHERE s.student_name LIKE ?
                       ORDER BY c.created_at DESC""",
                    (f"%{student_name_filter}%",)
                )
            else:
                self.cursor.execute(
                    """SELECT c.id, c.student_id, c.certificate_image_path, c.note, c.created_at,
                              s.student_name
                       FROM certificates c
                       JOIN students s ON c.student_id = s.id
                       ORDER BY c.created_at DESC"""
                )
            
            return self.cursor.fetchall()
        finally:
            self.close()
    
    def delete_certificate(self, certificate_id):
        """Delete a certificate by ID"""
        try:
            self.connect()
            self.cursor.execute("DELETE FROM certificates WHERE id = ?", (certificate_id,))
            self.conn.commit()
            return True, "Certificate deleted successfully"
        except Exception as e:
            return False, str(e)
        finally:
            self.close()
