from rest_framework import serializers
from CAM2API.models import Camera


class CameraSerializer(serializers.Serializer):
	camera_id = serializers.IntegerField() # id from old database 
	# Geography: 
	city = serializers.CharField()
	state = serializers.CharField()
	country = serializers.CharField()
	# lat_lng NO SERIALIZER
	# Source Information:
	source = serializers.CharField()
	source_url = serializers.CharField() # URL of source (Not for image data!)
	# Time Information:
	date_added = serializers.DateTimeField()
	last_updated = serializers.DateTimeField() # Last known time a snapshot was downloaded
	# Camera Types (Non_ip or IP)
	camera_type = serializers.CharField()
	# More Info:
	description = serializers.CharField() # Description of the camera
	is_video = serializers.BooleanField() # True if camera is a video stream 
	framerate = serializers.FloatField() # Frame rate of the camera if known
	outdoors = serializers.NullBooleanField() # True if camera is outdoors Null if unknown.
	indoors = serializers.NullBooleanField() # True if the camera is indoors Null if unknown.
	traffic = serializers.NullBooleanField() # True if the camera is a traffic camera Null if unknown.
	inactive = serializers.NullBooleanField() # True if data cannot be accessed from the camera Null if unknown.
	resolution_w = serializers.IntegerField() # Resolution width determined automatically 
	resolution_h = serializers.IntegerField() # Resolution height determined automatically 


	# id = serializers.IntegerField(read_only=True)
	# title = serializers.CharField(required=False, allow_blank=True, max_length=100)
	# code = serializers.CharField(style={'base_template': 'textarea.html'})
	# linenos = serializers.BooleanField(required=False)
	# language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
	# style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

	def create(self, validated_data):
		"""
		Create and return a new 'Camera' instance, given the validated data.
		"""
		return Snippet.objects.create(**validated_data)

	def update(self, instance, validated_data):
		"""
		Update and return an existing 'Camera' instance, given the validated data.
		"""
		instance.camera_id = validated_data.get('camera_id', instance.camera_id) # id from old database 
		# Geography: 
		instance.city = validated_data.get('city', instance.city)
		instance.state = validated_data.get('state', instance.state)
		instance.country = validated_data.get('country', instance.country)
		# Source Information:
		instance.source = validated_data.get('source', instance.source)
		instance.source_url = validated_data.get('source_url', instance.source_url) # URL of source (Not for image data!)
		# Time Information:
		instance.date_added = validated_data.get('date_added', instance.date_added)
		instance.last_updated = validated_data.get('last_updated', instance.last_updated) # Last known time a snapshot was downloaded
		# Camera Types (Non_ip or IP)
		instance.camera_type = validated_data.get('camera_type', instance.camera_type) 
		# More Info:
		instance.description = validated_data.get('description', instance.description) # Description of the camera
		instance.is_video = validated_data.get('is_video', instance.is_video) # True if camera is a video stream 
		instance.framerate = validated_data.get('framerate', instance.framerate) # Frame rate of the camera if known
		instance.outdoors = validated_data.get('outdoors', instance.outdoors) # True if camera is outdoors Null if unknown.
		instance.indoors = validated_data.get('indoors', instance.indoors) # True if the camera is indoors Null if unknown.
		instance.traffic = validated_data.get('traffic', instance.traffic) # True if the camera is a traffic camera Null if unknown.
		instance.inactive = validated_data.get('inactive', instance.inactive) # True if data cannot be accessed from the camera Null if unknown.
		instance.resolution_w = validated_data.get('resolution_w', instance.resolution_w) # Resolution width determined automatically 
		instance.resolution_h = validated_data.get('resolution_h', instance.resolution_h) # Resolution height determined automatically 

		instance.save()
		return instance