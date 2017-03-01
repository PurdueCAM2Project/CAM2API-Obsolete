from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Camera(models.Model):
	camera_id = models.PositiveIntegerField() # id from old database 
	# Geography: 
	city = models.CharField(max_length=30, null=False)
	state = models.CharField(max_length=12, null=True)
	country = models.CharField(max_length=50, null=False)
	# Source Information:
	source = models.CharField(max_length=30, null=False)
	source_url = models.CharField(max_length=100, null=False) # URL of source (Not for image data!)
	# Time Information:
	date_added = models.DateTimeField(auto_now_add=True)
	last_updated = models.DateTimeField() # Last known time a snapshot was downloaded
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
