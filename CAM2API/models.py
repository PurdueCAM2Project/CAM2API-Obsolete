from __future__ import unicode_literals

# from django.db import models
from django.contrib.gis.db import models # contrib.gis.db ensures the PostGis models are included

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

from django.conf import settings
from django.db.models.signals import post_save

from django.contrib.auth.signals import user_logged_in

from django.dispatch import receiver
from rest_framework.authtoken.models import Token 
from CAM2API.signals import account_created

# Camera Model
class Non_IP(models.Model):
	url = models.CharField(max_length=100, null=False) # URL to the image data 
	#camera = models.OneToOneField(Camera, blank=True, null=True, on_delete=models.CASCADE, related_name='NIP')
	#camera = GenericRelation(Camera)

class IP(models.Model):
	ip = models.CharField(max_length=44, null=False)
	port = models.PositiveIntegerField(null=True)
	# brand = models.PositiveIntegerField(null=True)
	# model = models.PositiveIntegerField(null=True)
	# video_path = models.CharField(max_length=100, null=False)
	# image_path = models.CharField(max_length=100, null=False)
	# rtsp_path = models.CharField(max_length=100, null=False)
	#camera = GenericRelation(Camera)
	#camera = models.OneToOneField(Camera, blank=True, null=True, on_delete=models.CASCADE, related_name='IP')

class Camera(models.Model):
	camera_id = models.PositiveIntegerField(unique=True) # id from old database 
	# Geography: 
	
	city = models.CharField(max_length=30, null=False)
	state = models.CharField(max_length=12, null=True, blank=True)
	country = models.CharField(max_length=50, null=False)
	lat = models.FloatField(max_length=100, null=False)
	lng = models.FloatField(max_length=100, null=False)
	lat_lng = models.GeometryField(geography=True, default=0) # Sets geometry field points to geography in postgis
	

	
	# Source Information:
	source = models.CharField(max_length=30, null=False)
	source_url = models.CharField(max_length=100, null=False) # URL of the provider of the source (NOT for image data!)
	# Time Information:
	date_added = models.DateTimeField(auto_now_add=True)
	last_updated = models.DateTimeField() # Last known time a snapshot was downloaded
	# Camera Types (Non_ip or IP)
	CAMERA_TYPES = enumerate(['Non_IP', 'IP'])
	camera_type = models.CharField(max_length=10, null=False, choices=CAMERA_TYPES, default='Non_IP')
	# More Info:
	description = models.CharField(max_length=100, null=True) # Description of the camera
	is_video = models.BooleanField() # True if camera is a video stream 
	framerate = models.FloatField(max_length=100, null=True) # Frame rate of the camera if known
	outdoors = models.NullBooleanField() # True if camera is outdoors Null if unknown.
	indoors = models.NullBooleanField() # True if the camera is indoors Null if unknown.
	traffic = models.NullBooleanField() # True if the camera is a traffic camera Null if unknown.
	inactive = models.NullBooleanField() # True if data cannot be accessed from the camera Null if unknown.
	resolution_w = models.PositiveIntegerField(null=True) # Resolution width determined automatically 
	resolution_h = models.PositiveIntegerField(null=True) # Resolution height determined automatically 
	# created_by = # Token for user who added the camera to the database
	
	# Image Retrieval objects:
	# For more information see https://docs.djangoproject.com/en/1.10/ref/contrib/contenttypes/#generic-relations
	
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, related_name="retrieval_model") #ContentType table incudes Class<Non_IP> as well as Class<IP>
	object_id = models.PositiveIntegerField(null=True) #object_id will be automatically generated and represents the sepecfic primary key for each object in the queryset 
	retrieval_model = GenericForeignKey('content_type', 'object_id')
	
	#ip = models.ForeignKey(IP, blank=True, null=True, on_delete=models.CASCADE, related_name="retrieval_model_ip")
	#non_ip = models.ForeignKey(Non_IP, blank=True, null=True, on_delete=models.CASCADE, related_name="retrieval_model_non_ip")


	#def __str__(self):
	#	return "camera_id: {}, camera_type: {}, image_retrieval: {}".format(camera_id, camera_type, image_retrieval)

class AccountManager(BaseUserManager):
	use_in_migration = True
		
	def _create_user(self, email, password, **extra_fields):
		email = self.normalize_email(email)
		account = self.model(email=email, **extra_fields)
		account.set_password(password)
		account.save(using=self._db)
		return account 

	def create_user(self, email, password, **extra_fields):
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_superuser', True)
		return self._create_user(email, password, **extra_fields)



class Record(models.Model):
	#username = models.CharField(max_length=20, null=False)
	permission = models.CharField(max_length=120, null=False)
	token = models.CharField(max_length=120, null=False)
	

class Account(AbstractUser):
	username = models.CharField(max_length=20, null=False)
	email = models.EmailField(unique=True)
	last_login = models.DateTimeField(auto_now_add=True)
	
	objects = AccountManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []



# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, **kwargs):
# 	if kwargs.get('created', False):
# 		account = kwargs.get('instance', None)
# 		if account is not None:
# 			token = Token.objects.create(user=account)
# 			username =  account.username
# 			print(dir(account))
# 			if account.is_superuser is True:
# 				permission = 'superuser'
# 			else:
# 				permission = 'base'
# 			record = Record.objects.create(username=username, token=token, permission=permission)
# 			record.save()
# 		print(Token.objects.get(user=kwargs.get('instance', None)).key)


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, **kwargs):
# 	if kwargs.get('created', False):
# 		account = kwargs.get('instance', None)
# 		if account is not None:
# 			Token.objects.create(user=account)
# 		print(Token.objects.get(user=kwargs.get('instance', None)).key)

#@receiver(user_logged_in, sender=settings.AUTH_USER_MODEL)
#def create_temp_token(sender, **kwargs):
#	account = kwargs.get('user', None)
#	if account:
#		Token.objects.create(user=account)
#		print(Token.objects)

#user_logged_in.connect(create_temp_token, sender=Account)





#post_save.connect(create_auth_token, sender=Account)

#class Account(AbstractUser):
#	pass
	#def create_account(self, username):
	#	account_created.send(sender = self.__class__, username)
	



