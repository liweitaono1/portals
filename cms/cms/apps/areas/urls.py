from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^addresses/$', views.Addresses.as_view({"get": "list", "post": "create"})),
    url(r'^addresses/(?P<pk>\d+)/$', views.Addresses.as_view({"delete": "destroy", "put": "update"})),
    url(r'^addresses/(?P<pk>\d+)/status/$', views.Addresses.as_view({"put": "status"})),

]
