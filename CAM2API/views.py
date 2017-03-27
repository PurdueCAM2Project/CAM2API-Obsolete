from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from rest_framework import status

# Import Models
from CAM2API.models import Camera
from CAM2API.serializers import CameraSerializer


@csrf_exempt
def camera_list(request):
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



@csrf_exempt
def camera_detail(request, pk):
	"""
	Retrieve, update or delete a code camera.
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