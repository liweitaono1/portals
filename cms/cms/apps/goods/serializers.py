from rest_framework import serializers

from .models import Goods, GoodsCategory, GoodsAlbum


class GoodsAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsAlbum
        fields = ["id", "thumb_path", "original_path"]


class GoodsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = ["id", 'title']


class CategorySerializer(serializers.ModelSerializer):
    parent = GoodsCategorySerializer(read_only=True)

    class Meta:
        model = GoodsCategory
        fields = ["id", "title", "parent"]


class GoodsSerializer(serializers.ModelSerializer):
    goodsalbum_set = GoodsAlbumSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Goods
        fields = '__all__'
