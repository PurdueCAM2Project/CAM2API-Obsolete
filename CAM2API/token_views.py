from rest_framework.authtoken.views import ObtainAuthToken
#from rest_framework.authtoken.models import Token 
from CAM2API.token import Token
from rest_framework.response import Response 
from CAM2API.token_serializers import CAM2TokenSerializer

class ObtainCAM2Token(ObtainAuthToken):
	serializer_class = CAM2TokenSerializer
	
	# def post(self, request, format=None):    #standard POST for acquring token
	# 	data = request.data
	# 	serializer = self.serializer_class(data=data)
	# 	if serializer.is_valid():
	# 		user = serializer.validated_data.get('user', None)
	# 		if user:
	# 			token, created = Token.objects.get_or_create(user=user)
	# 			return Response({'token': token.key})
	# 	return Response(serializer.errors)

	def post(self, request, format=None):
		data = request.data
		serializer = self.serializer_class(data=data)
		if serializer.is_valid():
			token = Token.objects.create()
			return Response({'Token': token.key})
		return Response(serializer.errors)

	def get(self, request, format=None):
		return Response({'detail':'GET method is not allowed'})



