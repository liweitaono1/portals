from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^areas/$', views.Area.as_view({"get": "list"})),
    url(r'areas/(?P<pk>\d+)/$', views.Area.as_view({"get": "retrieve"})),
]
