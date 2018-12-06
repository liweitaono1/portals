from rest_framework import serializers

from .models import Goods, GoodsCategory, GoodsAlbum


class GoodsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class SubGoodsCategorySerializer(serializers.ModelSerializer):
    # parent_id = GoodsCategorySerializer(read_only=True, many=True)
    goodscategory_set = GoodsCategorySerializer(many=True, read_only=True)

    class Meta:
        model = GoodsCategory
        fields = ['id', 'title', 'goodscategory_set']


class GoodsAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsAlbum
        fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):
    goodsalbum = GoodsAlbumSerializer(many=True, read_only=True)

    class Meta:
        model = Goods
        fields = ['goodsalbum', 'id', 'category_id', 'title', 'img_url', 'zhaiyao', 'status', 'is_slide',
                  'create_time', 'update_time', 'sub_title', 'goods_no', 'stock', 'market_price', 'sell_price',
                  'is_red', 'sales']
