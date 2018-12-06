from collections import OrderedDict

from django.shortcuts import render

# Create your views here.
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from rest_framework.views import APIView

from .models import Goods, GoodsCategory, GoodsAlbum
from .serializers import GoodsSerializer, GoodsCategorySerializer, SubGoodsCategorySerializer, GoodsAlbumSerializer


# URL:/goods/recommend/
class RecommendGoodsView(APIView):
    def get(self, request):
        good = Goods.objects.filter(is_red=1).order_by('-create_time')[0:4]
        serializer = GoodsSerializer(good, many=True)
        return Response(serializer.data)


# URL:/goods/category/
class GoodsCategoryView(APIView):
    def get(self, request):
        goodcategory = GoodsCategory.objects.filter(parent_id=0)
        serializer = SubGoodsCategorySerializer(goodcategory, many=True)
        for x in serializer.data:
            good = GoodsCategory.objects.filter(parent_id=x['id'])
            goods = []
            for y in good:
                serializer1 = GoodsSerializer(y.goods_set.all(), many=True)
                for z in serializer1.data:
                    goods.append(z)
            x['goods'] = goods
        return Response(serializer.data)


# URL:/goods/?Category=category_id&ordering=-create_time
class GoodsListView(APIView):
    filter_backends = (OrderingFilter,)
    order_fields = ('create_time', 'price', 'click')

    def get(self, request):
        category_id = request.query_params.get('category')
        goods = Goods.objects.filter(category_id=category_id)
        category = GoodsCategory.objects.filter(id=category_id)
        category = GoodsCategorySerializer(category, many=True)
        serializer = GoodsSerializer(goods, many=True)
        data = serializer.data
        goodsalbum_set = []
        for x in goods:
            goodsalbum = GoodsAlbum.objects.filter(goods_id=x.id)
            serializer1 = GoodsAlbumSerializer(goodsalbum, many=True)
            goodsalbum_set.append(serializer1.data)
        for x in data:
            x['category'] = category.data[0]
            id = x['category_id']
            parents = GoodsCategory.objects.filter(id=id)
            parent = GoodsCategorySerializer(parents, many=True)
            x['goodsalbum_set'] = goodsalbum_set[0]
            x['category']['parent'] = parent.data[0]

        return Response(data)


# /category/43/
class Categorys(APIView):
    def get(self, request, pk):
        category = GoodsCategory.objects.filter(id=pk)
        serializer = GoodsCategorySerializer(category, many=True)
        category = serializer.data
        id = category[0]['parent']
        parent = GoodsCategory.objects.filter(id=id)
        serializer = GoodsCategorySerializer(parent, many=True)
        category[0]['parent'] = serializer.data[0]
        return Response(category[0])


# URL: /goods/(?P<goods_id>\d+)/
class GoodsDetail(APIView):
    def get(self, request, goods_id):
        good = Goods.objects.filter(id=goods_id)
        goodscategory = GoodsCategory.objects.filter(id=good[0].category_id)
        serializer1 = GoodsCategorySerializer(goodscategory, many=True)

        serializer = GoodsSerializer(good, many=True)
        for x in serializer1.data:
            category = GoodsCategory.objects.filter(id=x['id'])
            serializer2 = GoodsCategorySerializer(category, many=True)
            parent_category = GoodsCategory.objects.filter(id=serializer2.data[0]['parent'])
            cndb = GoodsCategorySerializer(parent_category, many=True)
            serializer2.data[0]['parent'] = cndb.data[0]
        serializer.data[0]['category'] = serializer2.data[0]
        goodsalbum_set = []
        for x in good:
            goodsalbum = GoodsAlbum.objects.filter(goods_id=x.id)
            serializer1 = GoodsAlbumSerializer(goodsalbum, many=True)
            goodsalbum_set.append(serializer1.data)
        serializer.data[0]['goodsalbum_set'] = goodsalbum_set[0]
        return Response(serializer.data[0])


# URL: /goods/recommand/
class GoodsRecommend(APIView):
    def get(self, request):
        good = Goods.objects.filter(is_red=1).order_by('-create_time')[0:4]
        for x in good:
            print(x.create_time)
        serializer = GoodsSerializer(good, many=True)
        return Response(serializer.data)
