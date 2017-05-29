# Import Models and Serializer
from CAM2API.models import Camera, Non_IP, IP
from CAM2API.serializers import (CameraSerializer, IPSerializer, NonIPSerializer)

from django.contrib.gis.geos import GEOSGeometry

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404

class CameraList(APIView):
	"""
	Returns:
		GET - JSON response containing all the camera data in the database
		POST - Creates new camera objects in the database
	"""
	def get(self, request, format=None):
		"""
		Returns JSON response containing all the camera data in the database
		input request: HTTP GET request
		input format: optional format string included in HTTP request
		return: JSON String
		"""
		cameras = Camera.objects.all()
		serializer = IPCameraSerializer(cameras, many=True)
		return Response(serializer.data)

	
	def post(self, request, format=None):
		"""
		Creates new camera objects in the database and returns a HTTP 201 if success
		input request: HTTP POST request
		input format: optional format string included in HTTP request
		return: HTTP 201 if the data successfully saved in the database or HTTP 400 if
				there was an error saving the camera information to the database
		"""

		# try:
		# 	# Create the Geospacial Object:
		# 	lat_lng = '{{ "type": "Point", "coordinates": [ {}, {} ] }}'.format(request.data['lat'], request.data['lng'])
		# 	lat_lng = GEOSGeometry(lat_lng)
		# 	data = request.data
		# 	if 'url' in data.keys():
		# 		print("Here")
		# 		serializer = NonIPCameraSerializer(data=data)
		# 	else:
		# 		print("THere")
		# 		serializer = IPCameraSerializer(data=data)
		# 	#serializer = CameraSerializer(data=data)

		# except:
		# 	#return(Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST))
		# 	raise Http404
			
		# if serializer.is_valid():
		# 	serializer.save()
		# 	return(Response(serializer.data, status=status.HTTP_201_CREATED))
		# #print(type(data))
		# #print(type(serializer.data))
		# return(Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST))


		#lat_lng = '{{ "type": "Point", "coordinates": [ {}, {} ] }}'.format(request.data['lat'], request.data['lng'])
		#lat_lng = GEOSGeometry(lat_lng)	
		#data = self.convert_data(request.data)
		#print(data)
		#data.update({"lat_lng":lat_lng})
		'''
		if 'url' in data.keys():
			non_ip_serializer = NonIPSerializer(data=data)
			if non_ip_serializer.is_valid():
				data['retrieval_model'] = non_ip_serializer.data
				serializer = NonIPCameraSerializer(data=data)
		else:
			#ip_serializer = IPSerializer(data=data)
			#if ip_serializer.is_valid():
			#	print("First")
			#	ip_serializer.save()
			#	data['retrieval_model'] = ip_serializer.data
				sub_data = {}
				sub_data["ip"] = data.get("ip", None)
				sub_data["port"] = data.get("port", None)
				data['retrieval_model'] = sub_data
				serializer = IPCameraSerializer(data=data)
		'''
		data = self.convert_data(request.data)
		serializer = CameraSerializer(data=data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:	
			return Response(serializer.errors)

	def convert_data(self,data):     #needs further modification to make it more explicit
		if "url" in data.keys():
			url = data.pop("url")
			data["retrieval_model"] = {"url":url}
		elif "port" and "ip" in data.keys():
			port = data.pop("port")
			ip = data.pop("ip")
			data["retrieval_model"] = {"ip":ip, "port":port}		
		return data 

class CameraDetail(APIView):
	"""
	Retrieve, update or delete a specific camera in the database biased on camera ID 
		from the original database
	"""

	lookup_field = ['camera_id']
	lookup_url_kwargs = ['cd']

	# def get_object(self):
	# 	"""
	# 	Quarries that database for a camera object matching the pk given. 
	# 	This will search for cameras biased on the id given to them in the old database
	# 	returns: Camera object 
	# 	"""
	# 	try:
	# 		return Camera.objects.get(camera_id=pk)
	# 	except Camera.DoesNotExist:
	# 		raise Http404

	def get_object(self):
		lookup_url_kwargs = self.lookup_url_kwargs
		lookup_url_kwargs_value = [self.kwargs[item] for item in lookup_url_kwargs]
		filter_kwargs = dict(zip(self.lookup_field, lookup_url_kwargs_value))
		instance = get_object_or_404(Camera, **filter_kwargs) #the same as instance = get_object_or_404(Camera, camera_id=cd)
		return instance

	def get(self, request, cd, format=None):
		"""
		Handles HTTP GET requests to a specific camera in the database
		input request: the HTTP GET request sent to the API
		input pk: primary key of the camera in question.
		input format: optional format string included in HTTP request
		return: JSON/API response containing the relevant camera data or a HTTP 404 error
				if there is no camera that matches the pk 
		"""
		camera = self.get_object()
		serializer = CameraSerializer(camera)
		return(Response(serializer.data))


	def put(self, request, cd, pk, format=None):
		"""
		Handles HTTP PUT requests to a specific camera in the database and modifies the 
			given camera object in the database
		input request: the HTTP PUT request sent to the API
		input pk: primary key of the camera in question.
		input format: optional format string included in HTTP request
		return: Response containing the relevant camera data if the request is successful 
				or a HTTP 400 error if the camera cannot be edited to the database
		"""
		camera = self.get_object()
		try:
			lat_lng_point = '{{"type": "Point", "coordinates": [{}, {}]}}' .format(request.data['lat'], request.data['lng'])
			lat_lng = GEOSGeometry(lat_lng_point)
			data = request.data
			data['lat_lng'] = lat_lng
		except:
			raise Http404

		serializer = CameraSerializer(camera, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return(Response(serializer.data))
		return(Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST))


	def delete(self, request, cd, pk, format=None):
		"""
		Handles HTTP DELETE requests to a specific camera in the database
		input request: the HTTP DELETE request sent to the API
		input pk: primary key of the camera in question.
		input format: optional format string included in HTTP request
		return: Response containing the relevant camera data if the request is successful 
				or a HTTP 204 error if the camera is deleted from the database
		"""
		camera = self.get_object()
		camera.delete()
		return(Response(status=status.HTTP_204_NO_CONTENT))


# class CameraRetrieveMixin(obejct):
# 	def retrieve(self, request, *args, **kwargs):
# 		instance = self.get_object()
# 		serializer = self.get_serializer(instance)
# 		return Response(serializer.data)
