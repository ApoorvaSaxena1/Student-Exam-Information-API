from flask import Flask, jsonify
import json 
import threading
from sseclient import SSEClient
from config import * 

# Function is responsible for updating the in-memory databases (studentDatabase and examDatabase) 
# used by Rest APIs 
def fetchDataFromServer():  
  try:
    messages = SSEClient("http://live-test-scores.herokuapp.com/scores")
    for msg in messages:
      if msg.data:
        json_ht={}
        # Parse latest data from server stream event to json object
        json_obj=json.loads(msg.data)
        # Update the examDatabase
        if json_obj['exam'] not in app.examDatabase:
          app.examDatabase[json_obj['exam']]=[json_obj['score']]
        else:
          app.examDatabase[json_obj['exam']].append(json_obj['score'])
        # Update the studentDatabase
        if json_obj['studentId'] not in app.studentDatabase:
          app.studentDatabase[json_obj['studentId']]=[[json_obj['exam'],json_obj['score']]]
        else:
          app.studentDatabase[json_obj['studentId']].append([json_obj['exam'],json_obj['score']])
  except:
    print("No data received from External server")



"""
This function returns the student ids of all the students stored in the database
URL format for this API will be http://127.0.0.1:5000/students
For example : http://127.0.0.1:5000/students
"""
@app.route('/students', methods=['GET'])
def get_task():

  try:
    returnStr=""
    for key in app.studentDatabase:
      returnStr+=key+"\n"
    return returnStr
  except IOError:
    print('no internet')

"""
This function takes student id as argument and returns the average score. 
URL format for this API will be http://127.0.0.1:5000/students/<id>
For example : http://127.0.0.1:5000/students/Dandre.Hoeger
"""
@app.route('/students/<string:id>', methods=['GET'])
def get_task_by_id(id):
  try:
      if id in app.studentDatabase:
        arr=app.studentDatabase[id]
        return "Average score of student "+str(id)+" "+str(sum([x[1] for x in arr])/len(arr))
      else:
        return "No record of student "+str(id)
    
    
  except IOError:
    print('no internet')

"""
This function returns all exams taken by students so far.
URL format for this API will be http://127.0.0.1:5000/exams
For example : http://127.0.0.1:5000/exams
"""

@app.route('/exams', methods=['GET'])
def get_exam_list():
  try:
      returnStr="List of exams\n"
      for i in app.examDatabase:
        returnStr+=str(i)
        returnStr+="\n"

      return returnStr
    
    
  except IOError:
    print('no internet')


"""
This function takes exam id as an argument checks the database for scores of all the student 
who took this exam and returns the average.
URL format for this API will be http://127.0.0.1:5000/exams/<id>
For example : http://127.0.0.1:5000/exams/11399
"""

@app.route('/exams/<string:id>', methods=['GET'])
def get_exam_scores(id):
  try:
      if int(id) in app.examDatabase:
        arr=app.examDatabase[int(id)]
        returnStr="Average score for exam "+str(id)+" is "+str(sum(arr)/len(arr))+"\n"
        returnStr+="Score list:\n"
        for i in arr:
          returnStr+=str(i)+"\n"

        return returnStr
      else:
        return "Exam id not present"
    
    
  except IOError:
    print('no internet')


"""
This function starts the Flasks Service

"""

def startRestAPI():
  app.run()


"""
When this program is run, it will spawn 2 threads:

1) dataThread:    This thread calls the function responsible for fetching data from the external server
                  which is http://live-test-scores.herokuapp.com/scores

2) restAPIThread: This thread will start the flask server 

"""

if __name__ == '__main__':
  dataThread = threading.Thread(target=fetchDataFromServer, args=())
  restAPIThread = threading.Thread(target=startRestAPI, args=())
  dataThread.start()
  restAPIThread.start()
