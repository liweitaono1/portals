from collections import OrderedDict

from django.shortcuts import render

# Create your views here.
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from rest_framework.views import APIView

from .models import Goods, GoodsCategory, GoodsAlbum
from .serializers import GoodsSerializer, GoodsCategorySerializer, GoodsAlbumSerializer, \
    CategorySerializer


# URL:/goods/recommend/
class RecommendGoodsView(APIView):
    def get(self, request):
        good = Goods.objects.filter(is_red=1).order_by('-create_time')
        serializer = GoodsSerializer(good[0:4], many=True)
        return Response(serializer.data)


# URL:/goods/category/
class GoodsCategoryView(APIView):
    def get(self, request):
        categories = GoodsCategory.objects.filter(parent_id=0)
        data = []
        for category_1 in categories:
            goods = []
            goodscategory_set = []
            categories2 = category_1.goodscategory_set.all()
            for category_2 in categories2:
                category2 = {
                    'id': category_2.id,
                    'title': category_2.title,
                }
                goodscategory_set.append(category2)

                category_goods = Goods.objects.filter(category_id=category_2.id)
                serializer = GoodsSerializer(category_goods, many=True)
                goods.extend(serializer.data)

            category1 = {
                "id": category_1.id,
                "title": category_1.title,
                "goodscategory_set": goodscategory_set,
                "goods": goods
            }
            data.append(category1)

        return Response(data)

# URL:/goods/?Category=category_id&ordering=-create_time
class GoodsListView(ListAPIView):
    """
    商品列表页显示
    """
    serializer_class = GoodsSerializer

    filter_backends = (OrderingFilter,)
    ordering_fields = ('create_time', 'sell_price', 'sales')

    def get_queryset(self):
        Category_id = self.request.query_params.get('category')
        goods = Goods.objects.filter(category_id=Category_id)
        return goods

    # /category/43/


class Categorys(APIView):
    def get(self, request, pk):
        category = GoodsCategory.objects.get(id=pk)
        category = CategorySerializer(category).data
        return Response(category)


# URL: /goods/(?P<goods_id>\d+)/
class GoodsDetail(APIView):
    def get(self, request, goods_id):
        good = Goods.objects.get(id=goods_id)
        serializer = GoodsSerializer(good)
        return Response(serializer.data)


# URL: /goods/recommand/
class GoodsRecommend(APIView):
    def get(self, request):
        good = Goods.objects.filter(is_red=1).order_by('-create_time')[0:4]
        for x in good:
            print(x.create_time)
        serializer = GoodsSerializer(good, many=True)
        return Response(serializer.data)
