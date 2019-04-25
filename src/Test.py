from config import *
import Application
import unittest

class TestRestAPI(unittest.TestCase):
	def setUp(self):
		
		app.studentDatabase={'Dandre.Hoeger': [[8480, 0.8082767556887278]], 'Gaetano_Medhurst57': [[8480, 0.7343426771390034]]}
		app.examDatabase={8480:[0.8082767556887278,0.7343426771390034]}
		self.app=app.test_client()


	def test_get_task(self):
		rv = self.app.get('/students')
		assert rv.status == '200 OK'
		assert b'Dandre.Hoeger' in rv.data
		assert b'Gaetano_Medhurst57' in rv.data

	def test_get_task_by_id(self):
		rv = self.app.get('/students/Dandre.Hoeger')
		assert rv.status == '200 OK'
		assert "0.8082767556887278" in str(rv.data)

	def test_get_exam_list(self):
		rv = self.app.get('/exams')
		assert rv.status == '200 OK'
		assert "8480" in str(rv.data)

	def test_get_exam_scores(self):
		rv = self.app.get('/exams/8480')
		assert rv.status == '200 OK'
		assert "0.7713097164138656" in str(rv.data)
		

if __name__ == '__main__':
    unittest.main()