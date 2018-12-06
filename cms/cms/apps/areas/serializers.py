import re

from rest_framework import serializers

from .models import Address


class UserAddressesSerializer(serializers.ModelSerializer):
    province = serializers.StringRelatedField(label='省份名称', read_only=True)
    city = serializers.StringRelatedField(label='市区名称', read_only=True)
    district = serializers.StringRelatedField(label='县名称', read_only=True)
    province_id = serializers.IntegerField(label='省份id', write_only=True)
    city_id = serializers.IntegerField(label='城市id', write_only=True)
    district_id = serializers.IntegerField(label='县id', write_only=True)

    class Meta:
        model = Address
        exclude = ['user', 'is_deleted', 'create_time', 'update_time']

    def validate_mobile(self, value):
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机格式不正确')
        return value

    def create(self, validated_data):
        return Address.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', '')
        instance.receiver = validated_data.get('receiver', '')
        instance.province_id = validated_data.get('province_id', '')
        instance.city_id = validated_data.get('city_id', '')
        instance.district_id = validated_data.get('district_id', '')
        instance.place = validated_data.get('place', '')
        instance.mobile = validated_data.get('mobile', '')
        instance.tel = validated_data.get('tel', '')
        instance.email = validated_data.get('email', '')
        instance.save()

        return instance
