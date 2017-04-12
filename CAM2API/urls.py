from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from CAM2API import views

urlpatterns = [
    url(r'^cameras/$', views.camera_list),
    url(r'^cameras/(?P<pk>[0-9]+)/$', views.camera_detail),
]

# Adds format patterns to the API
urlpatterns = format_suffix_patterns(urlpatterns)