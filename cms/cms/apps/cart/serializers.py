from rest_framework import serializers

from goods.models import Goods


class CartSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(label='数量', min_value=1, read_only=True)
    selected = serializers.BooleanField(label='是否勾选', read_only=True)

    class Meta:
        model = Goods
        fields = ['id', 'count', 'title', 'market_price', 'sell_price', 'img_url', 'selected']
