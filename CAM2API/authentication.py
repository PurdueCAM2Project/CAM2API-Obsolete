from CAM2API.models import Account
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
import datetime 
from django.utils import timezone

class AccountTokenAuthentication(TokenAuthentication):
	def get_model(self):
		if self.model is not None:
			return self.model
		else:
			from CAM2API.token import Token
			return Token 

	# def authenticate_credentials(self, key):   #Authentiacation with expire feature
	# 	print('Authenticating')
	# 	model = self.get_model()

	# 	try:
	# 		token = model.objects.select_related('user').get(key=key)
	# 	except model.DoesNotExist:
	# 		raise exceptions.AuthenticationFailed('Invalid token')

	# 	if not token.user.is_active:
	# 		raise exceptions.AuthenticationFailed('User is not active')

	# 	current_time = timezone.now()
	# 	span = datetime.timedelta(minutes=2)

	# 	print(token.created)

	# 	if token.created < (current_time - span):
	# 		print('Delete')
	# 		token.delete()
	# 		raise exceptions.AuthenticationFailed('Token has expired')

	# 	return (token.user, token)

	def authenticate_credentials(self, key):
		print("Authenticating")
		model = self.get_model()

		try:
			token = model.objects.get(key=key)
		except model.DoesNotExist:
			raise exceptions.AuthenticationFailed('Invalid Token')

		#counter feature(potentially could be used later as seesion token)


		token_access_times = token.access_times + 1
		token.access_times = token_access_times
		token.save()

		if token_access_times > 10000:
			token.delete()
			raise exceptions.AuthenticationFailed('Token has hit its limit')
		
		#expiring feature(potentially could be used later as session token)

		current_time = timezone.now()
		timespan = datetime.timedelta(days=3000)

		if token.created < (current_time - timespan):
				print('Delete')
				token.delete()
				raise exceptions.AuthenticationFailed('Token has expired please request for a new one')

		return (None, token)  #Our token model does not associate with user



