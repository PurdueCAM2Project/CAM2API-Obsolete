from rest_framework import serializers
from django.contrib.auth import authenticate 

class CAM2TokenSerializer(serializers.Serializer):
	'''
	The backend of WebUI sends a HTTP request with a particular password embedded in the body(ref = "CAM2API"). 
	Then, the API would sends back a random string containing no personal information as the static access token. 
	Also, API would create a record in the database for future authenticaion and granting permission for access.
	'''
	ref = serializers.CharField(max_length=20)

	def validate(self, data):
		ref = data.get('ref', None)
		if ref:
			if ref != "CAM2API":
				raise serializers.ValidationError('Cheater')
		else:
			raise serializers.ValidationError('Please provide ref')
		return data
