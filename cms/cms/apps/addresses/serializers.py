from rest_framework import serializers

from .models import Areas


class AreasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Areas
        fields = ['id', 'name']


class AreasSubsSerializer(serializers.ModelSerializer):
    subs = AreasSerializer(many=True, read_only=True)

    class Meta:
        model = Areas
        fields = ['id', 'name', 'subs']
