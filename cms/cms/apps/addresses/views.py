from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from .models import Areas
from .serializers import AreasSerializer, AreasSubsSerializer


class Area(ViewSet):
    def list(self, request):
        province = Areas.objects.filter(parent=None)
        serializer = AreasSerializer(province, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        areas = Areas.objects.get(pk=pk)
        serializer = AreasSubsSerializer(instance=areas)
        return Response(serializer.data)
