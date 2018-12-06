from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^cart/$', views.Cart.as_view()),
    url(r'^cart/count/$', views.CARTCOUNT.as_view()),

]
