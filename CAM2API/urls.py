from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from CAM2API import views as camviews
from CAM2API import token_views
from django.contrib.auth import views as auth_view


urlpatterns = [
    url(r'^$', camviews.CameraList.as_view()),
    url(r'^cameras/$', camviews.CameraList.as_view()),
    url(r'^cameras/(?P<cd>[0-9]+)/$', camviews.CameraDetail.as_view(), name="retrieve_info"),
    url(r'^register/$', camviews.AccountCreate.as_view()),
    url(r'^login/$', camviews.AccountLogin.as_view()),
    url(r'^api-token-auth/$', token_views.ObtainCAM2Token.as_view(), name='obtain_token'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# Adds format patterns to the API
urlpatterns = format_suffix_patterns(urlpatterns)