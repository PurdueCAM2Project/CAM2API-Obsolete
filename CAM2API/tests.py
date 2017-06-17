from django.test import TestCase
# Create your tests here.
from django.core.management.base import BaseCommand
from CAM2API.models import Camera, Non_IP, IP
from django.contrib.gis.geos import GEOSGeometry
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.reverse import reverse
import json

'''
Fixed Test Cases Index

	#Basic Correctness Test
		#Data for Test Case C1 - Correct IP Camera Test
		#Data for Test Case C2 - Correct Non IP Camera Test

	#Missing Information Test
		#Data for Test Case E1 - Wrong IP Camera Without IP Test
		#Data for Test Case E2 - Correct IP Camera Without PORT Test
		#Data for Test Case E3 - Wrong Non IP Camera Without URL Test
		#Data for Test Case E4 - Wrong Camera With URL and IP Test
		#Data for Test Case E5 - Wrong Camera Without URL and IP Test
		#Data for Test Case E6 - Wrong Non IP Camera With URL and PORT Test
		#Data for Test Case E7 - Wrong Camera With URL, IP and PORT Test
		#Data for Test Case E8 - Wrong Camera Without ID Test
		#Data for Test Case E9 - Wrong Camera Without city Test
		#Data for Test Case E10 - Correct Camera Without state Test
		#Data for Test Case E11 - Wrong Camera Without Lag Test
		#Data for Test Case E12 - Wrong Camera Without lng Test
		#Data for Test Case E13 - Wrong Camera Without source Test
		#Data for Test Case E14 - Wrong Camera Without source_url Test


	#Uniqueness Test
		#Data for Test Case U1 - Wrong duplicated Camera ID Test

	#Non Exist Camera Test
		#Data for Test Case N1 - Wrong Camera ID to get Test
'''

class API_View_Tests(APITestCase):

	def setUp(self):
		
		#Basic Correctness Test

		#Data for Test Case C1 - Correct IP Camera Test
		self.data_C1 = {'lat':35.6895 ,'lng':139.6917,'city':'Shinjuku-ku','country':'JP','source':'google','source_url':'www.google.com','last_updated':'2016-04-15 07:41:52','description':'This is a test camera','is_video':1,'framerate':0.3,'outdoors':True,'indoors':False,'traffic':False,'inactive':False,'resolution_w':1920,'resolution_h':1080,'ip':"192.168.1.1",'port':8000, 'camera_id':8000}
		#Data for Test Case C2 - Correct Non IP Camera Test
		self.data_C2 = {'lat':35.6895 ,'lng':139.6917,'city':'Shinjuku-ku','country':'JP','source':'google','source_url':'www.google.com','last_updated':'2016-04-15 07:41:52','description':'This is a test camera','is_video':1,'framerate':0.3,'outdoors':True,'indoors':False,'traffic':False,'inactive':False,'resolution_w':1920,'resolution_h':1080,'url':'www.test.com','camera_id':8000}


		#Missing Information Test

		#Data for Test Case E1 - Wrong IP Camera Without IP Test
		self.data_E1 = {'lat':35.6895 ,'lng':139.6917,'city':'Shinjuku-ku','country':'JP','source':'google','source_url':'www.google.com','last_updated':'2016-04-15 07:41:52','description':'This is a test camera','is_video':1,'framerate':0.3,'outdoors':True,'indoors':False,'traffic':False,'inactive':False,'resolution_w':1920,'resolution_h':1080,'port':8000, 'camera_id':8000}

		#Data for Test Case E2 - Correct IP Camera Without PORT Test
		self.data_E2 = {'lat':35.6895 ,'lng':139.6917,'city':'Shinjuku-ku','country':'JP','source':'google','source_url':'www.google.com','last_updated':'2016-04-15 07:41:52','description':'This is a test camera','is_video':1,'framerate':0.3,'outdoors':True,'indoors':False,'traffic':False,'inactive':False,'resolution_w':1920,'resolution_h':1080,'ip':"192.168.1.1", 'camera_id':8000}

		#Data for Test Case E3 - Wrong Non IP Camera Without URL Test
		self.data_E3 = {'lat':35.6895 ,'lng':139.6917,'city':'Shinjuku-ku','country':'JP','source':'google','source_url':'www.google.com','last_updated':'2016-04-15 07:41:52','description':'This is a test camera','is_video':1,'framerate':0.3,'outdoors':True,'indoors':False,'traffic':False,'inactive':False,'resolution_w':1920,'resolution_h':1080, 'camera_id':8000}

		#Data for Test Case E4 - Wrong Camera With URL and IP Test
		self.data_E4 = {'lat':35.6895 ,'lng':139.6917,'city':'Shinjuku-ku','country':'JP','source':'google','source_url':'www.google.com','last_updated':'2016-04-15 07:41:52','description':'This is a test camera','is_video':1,'framerate':0.3,'outdoors':True,'indoors':False,'traffic':False,'inactive':False,'resolution_w':1920,'resolution_h':1080,'url':'www.test.com','ip':"192.168.1.1", 'camera_id':8000}

		#Data for Test Case E5 - Wrong Camera Without URL and IP Test
		self.data_E5 = {'lat':35.6895 ,'lng':139.6917,'city':'Shinjuku-ku','country':'JP','source':'google','source_url':'www.google.com','last_updated':'2016-04-15 07:41:52','description':'This is a test camera','is_video':1,'framerate':0.3,'outdoors':True,'indoors':False,'traffic':False,'inactive':False,'resolution_w':1920,'resolution_h':1080, 'camera_id':8000}

		#Data for Test Case E6 - Wrong Non IP Camera With URL and PORT Test
		self.data_E6 = {'lat':35.6895 ,'lng':139.6917,'city':'Shinjuku-ku','country':'JP','source':'google','source_url':'www.google.com','last_updated':'2016-04-15 07:41:52','description':'This is a test camera','is_video':1,'framerate':0.3,'outdoors':True,'indoors':False,'traffic':False,'inactive':False,'resolution_w':1920,'resolution_h':1080,'url':'www.test.com','port':8000, 'camera_id':8000}

		#Data for Test Case E7 - Wrong Camera With URL, IP and PORT Test
		self.data_E7 = {'lat':35.6895 ,'lng':139.6917,'city':'Shinjuku-ku','country':'JP','source':'google','source_url':'www.google.com','last_updated':'2016-04-15 07:41:52','description':'This is a test camera','is_video':1,'framerate':0.3,'outdoors':True,'indoors':False,'traffic':False,'inactive':False,'resolution_w':1920,'resolution_h':1080,'url':'www.test.com','ip':"192.168.1.1",'port':8000, 'camera_id':8000}

		#Data for Test Case E8 - Wrong Camera Without ID Test
		self.data_E8 = {'lat':35.6895 ,'lng':139.6917,'city':'Shinjuku-ku','country':'JP','source':'google','source_url':'www.google.com','last_updated':'2016-04-15 07:41:52','description':'This is a test camera','is_video':1,'framerate':0.3,'outdoors':True,'indoors':False,'traffic':False,'inactive':False,'resolution_w':1920,'resolution_h':1080,'ip':"192.168.1.1",'port':8000}

		#Data for Test Case E9 - Wrong Camera Without city Test
		self.data_E9 = {'lat':35.6895 ,'lng':139.6917,'country':'JP','source':'google','source_url':'www.google.com','last_updated':'2016-04-15 07:41:52','description':'This is a test camera','is_video':1,'framerate':0.3,'outdoors':True,'indoors':False,'traffic':False,'inactive':False,'resolution_w':1920,'resolution_h':1080,'ip':"192.168.1.1",'port':8000, 'camera_id':8000}

		#Data for Test Case E10 - Correct Camera Without state Test(Not US)
		self.data_E10 = {'lat':35.6895 ,'lng':139.6917,'city':'Shinjuku-ku','country':'JP','source':'google','source_url':'www.google.com','last_updated':'2016-04-15 07:41:52','description':'This is a test camera','is_video':1,'framerate':0.3,'outdoors':True,'indoors':False,'traffic':False,'inactive':False,'resolution_w':1920,'resolution_h':1080,'ip':"192.168.1.1",'port':8000, 'camera_id':8000}

		#Data for Test Case E11 - Wrong Camera Without Lag Test
		self.data_E11 = {'lng':139.6917,'city':'Shinjuku-ku','country':'JP','source':'google','source_url':'www.google.com','last_updated':'2016-04-15 07:41:52','description':'This is a test camera','is_video':1,'framerate':0.3,'outdoors':True,'indoors':False,'traffic':False,'inactive':False,'resolution_w':1920,'resolution_h':1080,'ip':"192.168.1.1",'port':8000, 'camera_id':8000}

		#Data for Test Case E12 - Wrong Camera Without lng Test
		self.data_E12 = {'lat':35.6895 ,'city':'Shinjuku-ku','country':'JP','source':'google','source_url':'www.google.com','last_updated':'2016-04-15 07:41:52','description':'This is a test camera','is_video':1,'framerate':0.3,'outdoors':True,'indoors':False,'traffic':False,'inactive':False,'resolution_w':1920,'resolution_h':1080,'ip':"192.168.1.1",'port':8000, 'camera_id':8000}

		#Data for Test Case E13 - Wrong Camera Without source Test
		self.data_E13 = {'lat':35.6895 ,'lng':139.6917,'city':'Shinjuku-ku','country':'JP','source_url':'www.google.com','last_updated':'2016-04-15 07:41:52','description':'This is a test camera','is_video':1,'framerate':0.3,'outdoors':True,'indoors':False,'traffic':False,'inactive':False,'resolution_w':1920,'resolution_h':1080,'ip':"192.168.1.1",'port':8000, 'camera_id':8000}

		#Data for Test Case E14 - Wrong Camera Without source_url Test
		self.data_E14 = {'lat':35.6895 ,'lng':139.6917,'city':'Shinjuku-ku','country':'JP','source':'google','last_updated':'2016-04-15 07:41:52','description':'This is a test camera','is_video':1,'framerate':0.3,'outdoors':True,'indoors':False,'traffic':False,'inactive':False,'resolution_w':1920,'resolution_h':1080,'ip':"192.168.1.1",'port':8000, 'camera_id':8000}


#Uniqueness Test
	#Data for Test Case U1 - Wrong duplicated Camera ID Test
		self.data_U1 = {'lat':35.6895 ,'lng':139.6917,'city':'Shinjuku-ku','country':'JP','source':'google','source_url':'www.google.com','last_updated':'2016-04-15 07:41:52','description':'This is a test camera','is_video':1,'framerate':0.3,'outdoors':True,'indoors':False,'traffic':False,'inactive':False,'resolution_w':1920,'resolution_h':1080,'ip':"192.168.1.1",'port':8000, 'camera_id':8000}
		
#Non Exist Camera Test
	#Data for Test Case N1 - Wrong Camera ID to get Test
		self.data_N1 = {'lat':35.6895 ,'lng':139.6917,'city':'Shinjuku-ku','country':'JP','source':'google','source_url':'www.google.com','last_updated':'2016-04-15 07:41:52','description':'This is a test camera','is_video':1,'framerate':0.3,'outdoors':True,'indoors':False,'traffic':False,'inactive':False,'resolution_w':1920,'resolution_h':1080,'ip':"192.168.1.1",'port':8000, 'camera_id':8000}

          

#Basic Correctness Test

	#Test Case C1 - Correct IP Camera Test
	def test_post_get_case_C1(self):
		client = APIClient()
		response = self.client.post('/cameras.json/',self.data_C1, format = 'json')
		print('post_test',response.content)
		self.assertEqual(response.status_code,200)
		response = self.client.get('/cameras/8000/')
		print('test', response.data)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['city'], 'Shinjuku-ku')

	#Test Case C2 - Correct Non IP Camera Test
	def test_post_get_case_C2(self):
		client = APIClient()
		response = self.client.post('/cameras.json/',self.data_C2, format = 'json')
		print('post_test',response.content)
		self.assertEqual(response.status_code,200)
		response = self.client.get('/cameras/8000/')
		print('test', response.data)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['city'], 'Shinjuku-ku')

	#Test Case E1 - Wrong IP Camera Without IP Test
	def test_post_get_case_E1(self):
		client = APIClient()
		response = self.client.post('/cameras.json/',self.data_E1, format = 'json')
		print('post_test',response.content)
		self.assertEqual(response.status_code,404)
		response = self.client.get('/cameras/8000/')
		print('test', response.data)
		self.assertEqual(response.status_code, 404)

	#Test Case E2 - Correct IP Camera Without PORT Test
	def test_post_get_case_E2(self):
		client = APIClient()
		response = self.client.post('/cameras.json/',self.data_E2, format = 'json')
		print('post_test',response.content)
		self.assertEqual(response.status_code,200)
		response = self.client.get('/cameras/8000/')
		print('test', response.data)
		self.assertEqual(response.status_code,200)
		self.assertEqual(response.data['city'], 'Shinjuku-ku')	

	#Test Case E3 - Wrong Non IP Camera Without URL Test
	def test_post_get_case_E3(self):
		client = APIClient()
		response = self.client.post('/cameras.json/',self.data_E3, format = 'json')
		print('post_test',response.content)
		self.assertEqual(response.status_code,404)
		response = self.client.get('/cameras/8000/')
		print('test', response.data)
		self.assertEqual(response.status_code,404)

	#Test Case E4 - Wrong Camera With URL and IP Test
	def test_post_get_case_E4(self):
		client = APIClient()
		response = self.client.post('/cameras.json/',self.data_E4, format = 'json')
		print('post_test',response.content)
		self.assertEqual(response.status_code,404)
		response = self.client.get('/cameras/8000/')
		print('test', response.data)
		self.assertEqual(response.status_code,404)

	#Test Case E5 - Wrong Camera Without URL and IP Test
	def test_post_get_case_E5(self):
		client = APIClient()
		response = self.client.post('/cameras.json/',self.data_E5, format = 'json')
		print('post_test',response.content)
		self.assertEqual(response.status_code,404)
		response = self.client.get('/cameras/8000/')
		print('test', response.data)
		self.assertEqual(response.status_code,404)

	#Test Case E6 - Wrong Non IP Camera With URL and PORT Test
	def test_post_get_case_E6(self):
		client = APIClient()
		response = self.client.post('/cameras.json/',self.data_E6, format = 'json')
		print('post_test',response.content)
		self.assertEqual(response.status_code,404)
		response = self.client.get('/cameras/8000/')
		print('test', response.data)
		self.assertEqual(response.status_code,404)

	#Test Case E7 - Wrong Camera With URL, IP and PORT Test
	def test_post_get_case_E7(self):
		client = APIClient()
		response = self.client.post('/cameras.json/',self.data_E7, format = 'json')
		print('post_test',response.content)
		self.assertEqual(response.status_code,404)
		response = self.client.get('/cameras/8000/')
		print('test', response.data)
		self.assertEqual(response.status_code, 404)

	#Test Case E8 - Wrong Camera Without ID Test
	def test_post_get_case_E8(self):
		client = APIClient()
		response = self.client.post('/cameras.json/',self.data_E8, format = 'json')
		print('post_test',response.content)
		self.assertEqual(response.status_code,404)
		response = self.client.get('/cameras/8000/')
		print('test', response.data)
		self.assertEqual(response.status_code, 404)

	#Test Case E9 - Wrong Camera Without city Test
	def test_post_get_case_E9(self):
		client = APIClient()
		response = self.client.post('/cameras.json/',self.data_E9, format = 'json')
		print('post_test',response.content)
		self.assertEqual(response.status_code,404)
		response = self.client.get('/cameras/8000/')
		print('test', response.data)
		self.assertEqual(response.status_code, 404)

	#Test Case E10 - Correct Camera Without state Test
	def test_post_get_case_E10(self):
		client = APIClient()
		response = self.client.post('/cameras.json/',self.data_E10, format = 'json')
		print('post_test',response.content)
		self.assertEqual(response.status_code,200)
		response = self.client.get('/cameras/8000/')
		print('test', response.data)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['city'], 'Shinjuku-ku')

	#Test Case E11 - Wrong Camera Without Lag Test
	def test_post_get_case_E11(self):
		client = APIClient()
		response = self.client.post('/cameras.json/',self.data_E11, format = 'json')
		print('post_test',response.content)
		self.assertEqual(response.status_code,404)
		response = self.client.get('/cameras/8000/')
		print('test', response.data)
		self.assertEqual(response.status_code, 404)

	#Data for Test Case E12 - Wrong Camera Without lng Test
	def test_post_get_case_E12(self):
		client = APIClient()
		response = self.client.post('/cameras.json/',self.data_E12, format = 'json')
		print('post_test',response.content)
		self.assertEqual(response.status_code,404)
		response = self.client.get('/cameras/8000/')
		print('test', response.data)
		self.assertEqual(response.status_code, 404)

	#Test Case E13 - Wrong Camera Without source Test
	def test_post_get_case_E13(self):
		client = APIClient()
		response = self.client.post('/cameras.json/',self.data_E13, format = 'json')
		print('post_test',response.content)
		self.assertEqual(response.status_code,404)
		response = self.client.get('/cameras/8000/')
		print('test', response.data)
		self.assertEqual(response.status_code, 404)

	#Test Case E14 - Wrong Camera Without source_url Test
	def test_post_get_case_E14(self):
		client = APIClient()
		response = self.client.post('/cameras.json/',self.data_E14, format = 'json')
		print('post_test',response.content)
		self.assertEqual(response.status_code,404)
		response = self.client.get('/cameras/8000/')
		print('test', response.data)
		self.assertEqual(response.status_code, 404)


#Uniqueness Test
	#Test Case U1 - Wrong duplicated Camera ID Test
	def test_post_get_case_U1(self):
		client = APIClient()
		#Post Once
		response = self.client.post('/cameras.json/',self.data_U1, format = 'json')
		print('post_test',response.content)
		self.assertEqual(response.status_code,200)
		#Post Twice
		response = self.client.post('/cameras.json/',self.data_U1, format = 'json')
		print('post_test',response.content)
		self.assertEqual(response.status_code,404)


#Non Exist Camera Test
	#Test Case N1 - Wrong Camera ID to get Test
	def test_post_get_case_N1(self):
		client = APIClient()
		response = self.client.post('/cameras.json/',self.data_N1, format = 'json')
		print('post_test',response.content)
		self.assertEqual(response.status_code,200)
		response = self.client.get('/cameras/8001/')
		print('test', response.data)
		self.assertEqual(response.status_code, 404)
