from __future__ import unicode_literals

# from django.db import models
from django.contrib.gis.db import models # contrib.gis.db ensures the PostGis models are included

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Camera Model
class Camera(models.Model):
	camera_id = models.PositiveIntegerField(unique=True) # id from old database 
	# Geography: 
	city = models.CharField(max_length=30, null=False)
	state = models.CharField(max_length=12, null=True)
	country = models.CharField(max_length=50, null=False)
	# float_lat = models.FloatField(max_length=100, null=True)
	# float_lng = models.FloatField(max_length=100, null=True)
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

	# Image Retrieval objects:
	# For more information see https://docs.djangoproject.com/en/1.10/ref/contrib/contenttypes/#generic-relations
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	retrieval_model = GenericForeignKey('content_type', 'object_id')

	def __str__(self):
		return "camera_id: {}, camera_type: {}, image_retrieval: {}".format(camera_id, camera_type, image_retrieval)

class Non_IP(models.Model):
	url = models.CharField(max_length=100, null=False) # URL to the image data 

class IP(models.Model):
	ip = models.CharField(max_length=44, null=False)
	port = models.PositiveIntegerField(null=True)
	brand = models.PositiveIntegerField(null=True)
	model = models.PositiveIntegerField(null=True)
	video_path = models.CharField(max_length=100, null=False)
	image_path = models.CharField(max_length=100, null=False)
	rtsp_path = models.CharField(max_length=100, null=False)