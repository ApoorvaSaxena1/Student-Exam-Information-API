from flask import Flask, jsonify

app = Flask(__name__)
# Dictionary containing student details with Student ID as key and exam,score as value
app.studentDatabase={}

# Dictionary containing exam details with Exam ID as key and array of scores as value
app.examDatabase={}
