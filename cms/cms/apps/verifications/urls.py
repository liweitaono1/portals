from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^sms_code/(?P<mobile>1[3-9]\d{9})/$', views.SMS_CODE.as_view())

]
