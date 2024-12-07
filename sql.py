import sqlite3

# Connect to sqlite
connection = sqlite3.connect("student.db")

# Create cursor to insert records
cursor = connection.cursor()

# Create table
table_info = """
CREATE TABLE student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    class INTEGER NOT NULL,
    marks FLOAT NOT NULL,
    section CHAR(1) NOT NULL
);
"""

# Execute the create table query
cursor.execute(table_info)

# Sample student records
students = [
    ('John Smith', 10, 85.5, 'A'),
    ('Emma Wilson', 10, 92.3, 'B'),
    ('Michael Brown', 11, 78.9, 'A'),
    ('Sarah Davis', 11, 95.7, 'C'),
    ('James Johnson', 10, 88.2, 'B')
]

# Insert query
insert_query = """
INSERT INTO student (name, class, marks, section)
VALUES (?, ?, ?, ?);
"""

# Insert multiple records
cursor.executemany(insert_query, students)

# Display inserted records
print("Inserted records:")
data = cursor.execute("SELECT * FROM student")

for row in data:
    print(row)

# Commit the changes
connection.commit()

# Close the connection
connection.close()
