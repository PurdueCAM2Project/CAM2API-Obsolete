from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from rest_framework import status
from rest_framework.decorators import api_view

# Import Models
from CAM2API.models import Camera
from CAM2API.serializers import CameraSerializer


@api_view(['GET', 'POST'])
def camera_list(request, format=None):
	"""
	Returns a list of all the cameras in the database for a HTTP GET request
	input request: the HTTP GET or POST request for the camera data
	return 	GET - JSON response containing all the camera data in the database
			POST - Creates new camera objects in the database
	"""
	if request.method == 'GET':
		cameras = Camera.objects.all()
		serializer = CameraSerializer(cameras, many=True)
		return JsonResponse(serializer.data, safe=False)

	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = CameraSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
		return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST'])
def camera_detail(request, pk, format=None):
	"""
	Retrieve, update or delete a specific camera in the database.
	input request: the HTTP GET or POST request sent to the API
	input pk: primary key of the camera in question. This will be set to the original
			database camera id for continuity.
	return: GET - JSON response containing the relevant camera data or a HTTP 204/400 error 
			if there is no camera that matches the pk
			PUT - adds a camera object to the database
			DELETE - removes the camera from the database.
	"""
	try:
		camera = Camera.objects.get(camera_id=pk)
	except Camera.DoesNotExist:
		return HttpResponse(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = CameraSerializer(camera)
		return JsonResponse(serializer.data)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = CameraSerializer(camera, data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data)
		return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method == 'DELETE':
		camera.delete()
		return HttpResponse(status=status.HTTP_204_NO_CONTENT)