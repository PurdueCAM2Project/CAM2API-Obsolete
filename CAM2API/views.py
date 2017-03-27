from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Import Models:
from CAM2API.models import Camera
from CAM2API.serializers import CameraSerializer


@api_view(['GET', 'POST'])
def camera_list(request):
	"""
    List all cameras, or create a new camera.
    """
	if request.method == 'GET':
		cameras = Camera.objects.all()
		serializer = CameraSerializer(cameras, many=True)
		return Response(serializer.data, safe=False)

	elif request.method == 'POST':
		serializer = CameraSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def camera_detail(request, pk):
	"""
	Retrieve, update or delete a camera object.
	"""
	try:
		camera = Camera.objects.get(camera_id=pk)
	except Camera.DoesNotExist:
		return HttpResponse(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = CameraSerializer(camera)
		return Response(serializer.data)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = CameraSerializer(camera, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method == 'DELETE':
		camera.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)