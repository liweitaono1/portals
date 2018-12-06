from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }


class UsernameMobileAuthBackend(ModelBackend):
    """
    自定义用户名或手机号认证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        users = User.objects.filter(Q(username=username) | Q(mobile=username))
        if users:
            user = users[0]
            if user.check_password(password):
                return user
