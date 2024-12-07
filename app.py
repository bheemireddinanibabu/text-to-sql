from dotenv import load_dotenv
load_dotenv()
import os
import sqlite3
import streamlit as st
import google.generativeai as genai

# Configure GenAI API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and provide sql query as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to retrieve query from sql db
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

# Define prompt
prompt = ["""
    You are an expert SQL query generator. I will provide you with a database schema and a question in natural language. Your task is to generate a correct SQL query based on the question.

    Database Schema:
    Table: student
    - id (INTEGER, Primary Key, Auto Increment)
    - name (TEXT)
    - class (INTEGER)
    - marks (FLOAT)
    - section (CHAR)
    - enrollment_date (DATE)

    Table: subjects
    - subject_id (INTEGER, Primary Key)
    - subject_name (TEXT)
    - teacher_id (INTEGER)

    Table: student_subjects
    - student_id (INTEGER, Foreign Key -> student.id)
    - subject_id (INTEGER, Foreign Key -> subjects.subject_id)
    - marks (FLOAT)

    Rules and Guidelines:
    1. Generate only the SQL query without any explanations
    2. Use proper table aliases for better readability
    3. Use appropriate JOIN types (INNER, LEFT, RIGHT) based on requirements
    4. Include proper WHERE clauses for filtering
    5. Use GROUP BY and HAVING for aggregations when needed
    6. Consider performance by using indexes and optimized joins
    7. Handle NULL values appropriately using COALESCE or IFNULL
    8. Use proper date functions for date-related queries

    Example Questions and Expected Queries:

    Q: Show students and their subject marks
    A: SELECT s.name, sub.subject_name, ss.marks 
       FROM student s 
       JOIN student_subjects ss ON s.id = ss.student_id 
       JOIN subjects sub ON ss.subject_id = sub.subject_id;

    Q: Find average marks by subject
    A: SELECT sub.subject_name, AVG(ss.marks) as avg_marks 
       FROM subjects sub 
       LEFT JOIN student_subjects ss ON sub.subject_id = ss.subject_id 
       GROUP BY sub.subject_name;

    Q: List students who joined this year with marks above 80
    A: SELECT s.name, s.marks 
       FROM student s 
       WHERE s.marks > 80 
       AND YEAR(s.enrollment_date) = YEAR(CURRENT_DATE);
    the sql code should not  have ``` in beginning or end and sql word should not be there.
    Now, generate SQL query for the following question:
    """
]

# Streamlit app
st.set_page_config(page_title="SQL Query Generator")
st.header("SQL Query Generator")
question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit:
    response = get_gemini_response(question, prompt)
    st.subheader("The SQL Query is")
    st.write(response)
    st.subheader("The Result is")
    query = response
    answer = read_sql_query(query, "student.db")
    st.write(answer)
    st.subheader("The Answer is")
    for row in answer:
        st.write(row)


