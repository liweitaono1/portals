import re

from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(label='校验密码', write_only=True)
    sms_code = serializers.CharField(label='校验码', write_only=True)
    allow = serializers.BooleanField(label='是否同意协议', write_only=True)
    token = serializers.CharField(label='token', read_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'sms_code', 'mobile', 'allow', 'token']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 32,
            },
            'username': {
                'min_length': 5,
                'max_length': 20,
            }
        }

    def validate_mobile(self, value):
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机格式不正确')
        return value

    def validate_allow(self, value):
        if value == '0':
            raise serializers.ValidationError("请同意协议")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value):
            raise serializers.ValidationError('用户已存在')
        return value

    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs['password2']
        if password != password2:
            raise serializers.ValidationError('')
        sms = get_redis_connection('default')
        mobile = attrs['mobile']
        real_sms_code = sms.get('sms_code_%s' % mobile)
        if not real_sms_code:
            raise serializers.ValidationError('校验码失效')
        sms_code = attrs['sms_code']
        print(sms_code.lower(), real_sms_code.decode().lower())
        if sms_code != real_sms_code.decode():
            raise serializers.ValidationError('校验码无效')
        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_hander = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_hander(payload)
        user.token = token

        return user
