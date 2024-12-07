# database_setup.py
import sqlite3
from typing import List, Tuple
import os

class DatabaseSetup:
    def __init__(self, db_name: str = "student.db"):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            return True
        except sqlite3.Error as e:
            print(f"Database connection error: {str(e)}")
            return False

    def create_table(self):
        """Create student table"""
        if not self.cursor:
            if not self.connect():
                return False

        table_info = """
        CREATE TABLE IF NOT EXISTS student (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            class INTEGER NOT NULL,
            marks FLOAT NOT NULL,
            section CHAR(1) NOT NULL
        );
        """
        try:
            self.cursor.execute(table_info)
            self.connection.commit()
            print("Table created successfully!")
            return True
        except sqlite3.Error as e:
            print(f"Table creation error: {str(e)}")
            return False

    def insert_sample_data(self):
        """Insert sample student records"""
        if not self.cursor:
            if not self.connect():
                return False

        students = [
            ('John Smith', 10, 85.5, 'A'),
            ('Emma Wilson', 10, 92.3, 'B'),
            ('Michael Brown', 11, 78.9, 'A'),
            ('Sarah Davis', 11, 95.7, 'C'),
            ('James Johnson', 10, 88.2, 'B')
        ]

        insert_query = """
        INSERT INTO student (name, class, marks, section)
        VALUES (?, ?, ?, ?);
        """

        try:
            self.cursor.executemany(insert_query, students)
            self.connection.commit()
            print("Sample data inserted successfully!")
            return True
        except sqlite3.Error as e:
            print(f"Data insertion error: {str(e)}")
            return False

    def display_records(self):
        """Display all student records"""
        if not self.cursor:
            if not self.connect():
                return False

        try:
            self.cursor.execute("SELECT * FROM student")
            records = self.cursor.fetchall()

            if not records:
                print("\nNo records found.")
                return True

            print("\nStudent Records:")
            print("-" * 50)
            print("ID | Name | Class | Marks | Section")
            print("-" * 50)
            
            for row in records:
                print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")
            
            return True
                
        except sqlite3.Error as e:
            print(f"Data retrieval error: {str(e)}")
            return False

    def table_exists(self) -> bool:
        """Check if student table exists"""
        if not self.cursor:
            if not self.connect():
                return False

        try:
            self.cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='student'
            """)
            return bool(self.cursor.fetchone())
        except sqlite3.Error as e:
            print(f"Table check error: {str(e)}")
            return False

    def setup_database(self):
        """Complete database setup process"""
        try:
            # Connect to database
            if not self.connect():
                return
            
            # Check if table exists
            if self.table_exists():
                print("Table already exists!")
                self.cursor.execute("SELECT * FROM student")
                records = self.cursor.fetchall()
                if not records:
                    print("Table is empty!")
                    if not self.insert_sample_data():
                        return
            else:
                # Create table
                if not self.create_table():
                    return
                
                # Insert sample data
                if not self.insert_sample_data():
                    return
            
            # Display records
            self.display_records()
            
        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            # Close the connection
            if self.connection:
                self.connection.close()
                print("\nDatabase connection closed.")

    def clear_table(self):
        """Clear all records from the table"""
        if not self.cursor:
            if not self.connect():
                return False

        try:
            self.cursor.execute("DELETE FROM student")
            self.connection.commit()
            print("Table cleared successfully!")
            return True
        except sqlite3.Error as e:
            print(f"Table clear error: {str(e)}")
            return False

    def backup_database(self):
        """Create a backup of the database"""
        if not os.path.exists(self.db_name):
            print("Database file not found")
            return False

        try:
            backup_dir = "backups"
            os.makedirs(backup_dir, exist_ok=True)
            
            backup_file = f"{backup_dir}/student_backup.db"
            
            with sqlite3.connect(backup_file) as backup_conn:
                self.connection.backup(backup_conn)
                
            print(f"Database backed up to: {backup_file}")
            return True
            
        except Exception as e:
            print(f"Backup error: {str(e)}")
            return False