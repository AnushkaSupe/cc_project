import streamlit as st
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables
MONGO_URI = os.getenv('mongodb://localhost:27017')
print("MongoDB URI from .env file:", MONGO_URI)  # Add this line to print the MongoDB URI

# Check if MONGO_URI is not None
if MONGO_URI is None:
    st.error("MongoDB URI is not set. Please check your .env file.")
else:
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client.student_db
    collection = db.students

    # Streamlit UI
    st.title('Student Attendance Management System')

    option = st.sidebar.selectbox('Menu', ['Mark Attendance', 'View Attendance'])

    if option == 'Mark Attendance':
        name = st.text_input('Enter Student Name:')
        date = st.date_input('Select Date:')
        present = st.checkbox('Present')
        if st.button('Submit'):
            attendance = {'Name': name, 'Date': date, 'Present': present}
            collection.insert_one(attendance)
            st.success('Attendance marked successfully!')

    elif option == 'View Attendance':
        student_name = st.text_input('Enter Student Name:')
        if st.button('Search'):
            attendance_records = list(collection.find({'Name': student_name}))
            if attendance_records:
                attendance_df = pd.DataFrame(attendance_records)
                st.table(attendance_df)
            else:
                st.info('No attendance records found for this student.')
