import random

from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.views import APIView

from celery_tasks.sms.tasks import send_sms_code


class SMS_CODE(APIView):
    def get(self, request, mobile):
        sms = get_redis_connection('default')
        if sms.get('sms_flag_%s' % mobile):
            return Response({'message': '请在60秒后再次发送'})
        num = '%05d' % random.randint(0, 99999)
        send_sms_code.delay(mobile, num, 60 * 5)
        pip = sms.pipeline()
        pip.setex("sms_code_%s" % mobile, 5 * 60, num)
        pip.setex("sms_flag_%s" % mobile, 60, 1)
        pip.execute()
        return Response({"status": 1,"time":1})
