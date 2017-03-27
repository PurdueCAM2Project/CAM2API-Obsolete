from django.conf.urls import url
from CAM2API import views

urlpatterns = [
    url(r'^cameras/$', views.camera_list),
    url(r'^cameras/(?P<pk>[0-9]+)/$', views.camera_detail),
]