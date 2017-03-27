from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
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
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)



@csrf_exempt
def camera_detail(request, pk):
	"""
	Retrieve, update or delete a code camera.
	"""
	try:
		camera = Camera.objects.get(pk=pk)
	except Camera.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = CameraSerializer(camera)
		return JsonResponse(serializer.data)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = CameraSerializer(camera, data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data)
		return JsonResponse(serializer.errors, status=400)

	elif request.method == 'DELETE':
		camera.delete()
		return HttpResponse(status=204)