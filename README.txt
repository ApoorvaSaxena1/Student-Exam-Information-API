Student Exam Information API

System Requirements:
1. Python 3 or higher.
2. Open Source Libraries used :
	a) flask
	b) threading
	c) sseclient
	d) unittest
	e) json

How to run the application:

1. Run Application.py from the folder src.
2. Using curl command from command line or Postman widget try to hit the webservice.
   (The server will be running at 127.0.0.1:5000)
   127.0.0.1:5000/students
   127.0.0.1:5000/students/<student_name>
   127.0.0.1:5000/exams/
   127.0.0.1:5000/exams/<exam_id>


How to test the application:

1. Run Test.py from the src folder.
2. Result will be displayed on the terminal.
