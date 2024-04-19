import streamlit as st
import pandas as pd
from pymongo import MongoClient

# Set your MongoDB URI here
MONGO_URI = "mongodb+srv://anushkasupe1:8zDA5Q3QXRoIPYK5@cluster0.qfu1qzq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client.attendance_db
collection = db.attendance_records

# Streamlit UI
st.title('Attendance Management System')

option = st.sidebar.selectbox('Menu', ['Mark Attendance', 'View Attendance'])

if option == 'Mark Attendance':
    student_id = st.text_input('Enter Student ID:')
    status = st.radio('Attendance Status:', ('Present', 'Absent'))
    if st.button('Submit'):
        new_entry = {'StudentID': student_id, 'Status': status}
        collection.insert_one(new_entry)
        st.success('Attendance marked successfully!')

elif option == 'View Attendance':
    attendance_records = list(collection.find())
    if attendance_records:
        attendance_df = pd.DataFrame(attendance_records)
        st.table(attendance_df)
    else:
        st.info('No attendance records found.')

