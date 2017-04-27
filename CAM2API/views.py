# Import Models and Serializer
from CAM2API.models import Camera
from CAM2API.serializers import CameraSerializer

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class camera_list(APIView):
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
		serializer = CameraSerializer(cameras, many=True)
		return Response(serializer.data)


	def post(self, request, format=None):
		"""
		Creates new camera objects in the database and returns a HTTP 201 if success
		input request: HTTP POST request
		input format: optional format string included in HTTP request
		return: HTTP 201 if the data successfully saved in the database or HTTP 400 if
				there was an error saving the camera information to the database
		"""
		serializer = CameraSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return(Response(serializer.data, status=status.HTTP_201_CREATED))
		return(Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST))


class CameraDetail(APIView):
	"""
	Retrieve, update or delete a specific camera in the database biased on camera ID 
		from the original database
	"""
	def get_object(self, pk):
		"""
		Quarries that database for a camera object matching the pk given. 
		This will search for cameras biased on the id given to them in the old database
		returns: Camera object 
		"""
		try:
			return Camera.objects.get(camera_id=pk)
		except Camera.DoesNotExist:
			raise Http404


	def get(self, request, pk, format=None):
		"""
		Handles HTTP GET requests to a specific camera in the database
		input request: the HTTP GET request sent to the API
		input pk: primary key of the camera in question.
		input format: optional format string included in HTTP request
		return: JSON/API response containing the relevant camera data or a HTTP 404 error
				if there is no camera that matches the pk 
		"""
		camera = self.get_object(pk)
		serializer = CameraSerializer(camera)
		return(Response(serializer.data))


	def put(self, request, pk, format=None):
		"""
		Handles HTTP PUT requests to a specific camera in the database and modifies the 
			given camera object in the database
		input request: the HTTP PUT request sent to the API
		input pk: primary key of the camera in question.
		input format: optional format string included in HTTP request
		return: Response containing the relevant camera data if the request is successful 
				or a HTTP 400 error if the camera cannot be edited to the database
		"""
		camera = self.get_object(pk)
		serializer = CameraSerializer(camera, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return(Response(serializer.data))
		return(Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST))


	def delete(self, request, pk, format=None):
		"""
		Handles HTTP DELETE requests to a specific camera in the database
		input request: the HTTP DELETE request sent to the API
		input pk: primary key of the camera in question.
		input format: optional format string included in HTTP request
		return: Response containing the relevant camera data if the request is successful 
				or a HTTP 204 error if the camera is deleted from the database
		"""
		camera = self.get_object(pk)
		camera.delete()
		return(Response(status=status.HTTP_204_NO_CONTENT))
