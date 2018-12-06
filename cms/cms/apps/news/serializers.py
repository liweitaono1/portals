from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from .models import News, NewsCategory


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title']


class SubNewsCategorySerializer(serializers.ModelSerializer):
    newscategory_set = NewsCategorySerializer(many=True, read_only=True)
    news = NewsSerializer(many=True, read_only=True)
    top8 = NewsSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'newscategory_set', 'news', 'top8']
