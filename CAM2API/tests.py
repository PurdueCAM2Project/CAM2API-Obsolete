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


class APITests(APITestCase):

	def setUP_for_post(self):
		self.non_ip_data = {'camera_id':'52', 'lat':35.6895, 'lng':139.6917, 'city':'shinjuku-ku', 'state':'', 'country':'Japan', 'source':'google', 'source_url':'www.google.com', 'last_updated':'2016-04-15 07:41:52', 'description':'This is a non-ip camera', 'is_video':True, 'framerate':0.3, 'outdoors':True, 'indoors':False, 'traffic':False, 'inactive':False, 'resolution_w':1920, 'resolution_h':1080, 'camera_type':"Non_ip", 'url':'www.google.com'}
		self.ip_data = {'camera_id':'16','lat':40.4259, 'lng':86.9081, 'city':'West Lafayette', 'state':'Indiana', 'country':'United States', 'source':'google', 'source_url':'www.google.com', 'last_updated':'2016-04-15 07:41:52', 'description':'This is an ip camera', 'is_video':False, 'outdoors':False, 'indoors':True, 'traffic':True, 'inactive':True, 'resolution_w':1024, 'resolution_h':768, 'camera_type':"IP", 'ip':"192.168.1.1",'port':8000}
		
		#self.non_ip_data = {camera_id='52', lat_lng=lat_lng, lat=35.6895, lng=139.6917, city='Tokyo', state='', country='Japan', source='google', source_url='www.google.com', last_updated=timezone.now(), description='This is a non-ip camera', is_video=True, framerate=0.3, outdoors=True, indoors=False, traffic=False, inactive=False, resolution_w=1920, resolution_h=1080, camera_type="Non_ip", retrieval_model=im_uri}
		#self.ip_data = {camera_id='16', lat_lng=lat_lng, lat=40.4259, lng=86.9081, city='West Lafayette', state='Indiana', country='United States', source='google', source_url='www.google.com', last_updated=timezone.now(), description='This is an ip camera', is_video=False, outdoors=False, indoors=True, traffic=True, inactive=True, resolution_w=1024, resolution_h=768, camera_type="IP", retrieval_model=im_ip}

	def setUP_for_get(self):
		im_uri = Non_IP(url="www.example.com/image")
		im_uri.save()
		im_ip = IP(ip='10.0.0.1', port=80)
		lat_lng = GEOSGeometry('{ "type": "Point", "coordinates": [ 35.6895, 139.6917 ] }')
		self.test_non_ip_cam = Camera.objects.create(camera_id='52', lat_lng=lat_lng, lat=35.6895, lng=139.6917, city='Tokyo', state='', country='Japan', source='google', source_url='www.google.com', last_updated='2016-04-15 07:41:52', description='This is a non-ip camera', is_video=True, framerate=0.3, outdoors=True, indoors=False, traffic=False, inactive=False, resolution_w=1920, resolution_h=1080, camera_type="Non_ip", retrieval_model=im_uri)
		self.test_ip_cam = Camera.objects.create(camera_id='16', lat_lng=lat_lng, lat=40.4259, lng=86.9081, city='West Lafayette', state='Indiana', country='United States', source='google', source_url='www.google.com', last_updated='2016-04-15 07:41:52', description='This is an ip camera', is_video=False, outdoors=False, indoors=True, traffic=True, inactive=True, resolution_w=1024, resolution_h=768, camera_type="IP",  retrieval_model=im_ip)
		self.non_ip_data = {'camera_id':'52', 'lat':35.6895, 'lng':139.6917, 'city':'Tokyo', 'state':'', 'country':'Japan', 'source':'google', 'source_url':'www.google.com', 'last_updated':'2016-04-15 07:41:52', 'description':'This is a non-ip camera', 'is_video':True, 'framerate':0.3, 'outdoors':True, 'indoors':False, 'traffic':False, 'inactive':False, 'resolution_w':1920, 'resolution_h':1080, 'camera_type':"Non_ip", 'url':'www.google.com'}
		self.ip_data = {'camera_id':'16','lat':40.4259, 'lng':86.9081, 'city':'West Lafayette', 'state':'Indiana', 'country':'United States', 'source':'google', 'source_url':'www.google.com', 'last_updated':'2016-04-15 07:41:52', 'description':'This is an ip camera', 'is_video':False, 'outdoors':False, 'indoors':True, 'traffic':True, 'inactive':True, 'resolution_w':1024, 'resolution_h':768, 'camera_type':"IP", 'ip':'192.168.1.1', 'port':8000}

        
	def create(self):
		self.setUP_for_get()
		non_ip_test = Camera.objects.get(camera_id='52')
		ip_test = Camera.objects.get(camera_id ='16')
		self.assertEqual(non_ip_test, self.test_non_ip_cam)
		self.assertEqual(ip_test, self.test_ip_cam)


	def test_post(self):
		self.setUP_for_post()
		client = APIClient()
		#IP Camera Test - camtest
		response = self.client.post('/cameras.json/',self.non_ip_data, content_type = "application/json")
		self.assertEqual(response.status_code,status.HTTP_201_CREATED)
		#Non IP Camera Test
		response = self.client.post('/cameras.json/',self.ip_data, content_type = "application/json")
		self.assertEqual(response.status_code,status.HTTP_201_CREATED)


	def test_get(self):
		self.setUP_for_get()
		client = APIClient()
		#IP Camera Test
		response = self.client.get('/cameras/16/')
		self.assertEqual(response.status_code,status.HTTP_200_OK)
		self.assertEqual(response.data['city'], 'West Lafayette')   
		#Non IP Camera Test
		response = self.client.get('/cameras/52/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['city'], 'Tokyo')


