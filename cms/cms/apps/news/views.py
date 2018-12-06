from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import News, NewsCategory
from .serializers import NewsSerializer, NewsCategorySerializer, SubNewsCategorySerializer


class NewsView(APIView):
    def get(self, request):
        slide_news = News.objects.filter(is_slide=1)
        slideserializer = NewsSerializer(slide_news, many=True)
        top_news = News.objects.all().order_by('create_time')[0:10]
        topserializer = NewsSerializer(top_news, many=True)
        image_news = News.objects.exclude(img_url='').filter(Q(img_url__isnull=False)).order_by('click')[0:4]
        imageserializer = NewsSerializer(image_news, many=True)
        data = {
            'slide_news': slideserializer.data,
            'top_news': topserializer.data,
            'image_news': imageserializer.data,
        }
        return Response(data)


class NewsCategoryView(APIView):
    def get(self, request):

        cat = NewsCategory.objects.filter(parent_id=0)
        serializer = SubNewsCategorySerializer(cat, many=True)

        for x in serializer.data:
            news = []
            categories = x['id']
            category = NewsCategory.objects.filter(parent_id=categories)
            if len(category) == 3:
                command_news = News.objects.filter(
                    Q(category_id=category[0]) | Q(category_id=category[1]) | Q(category_id=category[2])).order_by(
                    "-create_time")
            else:
                command_news = News.objects.filter(
                    Q(category_id=category[0]) | Q(category_id=category[1])).order_by(
                    "-create_time")
            for y in category:
                new = News.objects.filter(Q(category_id=y) & Q(img_url__isnull=False))
                serializer1 = NewsSerializer(new, many=True)

                for z in serializer1.data:
                    if z['img_url'] == '':
                        continue
                    news.append(z)
            serializer2 = NewsSerializer(command_news, many=True)
            x['news'] = news[0:4]

            x['top8'] = serializer2.data

        return Response(serializer.data)
