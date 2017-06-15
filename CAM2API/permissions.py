from rest_framework import permissions, HTTP_HEADER_ENCODING, exceptions
from django.utils.six import text_type
from CAM2API.token import Token

def get_authorization_header(request):
	auth = request.META.get('HTTP_AUTHORIZATION', None)
	if auth:
		if isinstance(auth, text_type):
			auth = auth.encode(HTTP_HEADER_ENCODING)
	return auth

class CAM2APIPermission(permissions.BasePermission):
	#POST method is only valid for authenticated user and can only be edited by the object owner 
	#GET moethod is exposed to anyone

	def has_permission(self, request, view):
		auth = get_authorization_header(request)
		if auth is not None:
			(method, key) = auth.split()
			try:
				method = str(method, 'utf-8')
			except UnicodeError:
				raise exceptions.AuthenticationFailed("Invalid token header. Authentication method should not contain invalid characters")
			if method == "Token":
					try:
						key = str(key, 'utf-8')
					except UnicodeError:
						raise exceptions.AuthenticationFailed("Invalid token header. Token string should not contain invalid characters")
					token = Token.objects.get(key=key)
			else:
				raise exceptions.AuthenticationFailed("Invalid token header. The authentication method should be TokenAuthentication")
		else:
			raise exceptions.AuthenticationFailed("Invalid token header. The header does not exist")
		
		if request.method == 'GET':
			print("GET_Permission")
			return token and token.permission == 'SuperUser'

		elif request.method == 'POST':
			print("POST_Permission")
			return token and token.permission == 'SuperUser'


