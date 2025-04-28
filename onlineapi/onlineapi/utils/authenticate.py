from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend, UserModel
from django.db.models import Q
from django_redis import get_redis_connection


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        if hasattr(user, 'avatar'):
            token['avatar'] = user.avatar.url if user.avatar else ""
        if hasattr(user, 'nickname'):
            token['nickname'] = user.nickname
        if hasattr(user, 'money'):
            token['money'] = float(user.money)
        if hasattr(user, 'credit'):
            token['credit'] = user.credit
        try:
            redis = get_redis_connection("cart")
            token['cart_total'] = redis.hlen(f"cart_{user.id}")
        except Exception as e:
            token['cart_total'] = 0  # 或记录日志
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        redis = get_redis_connection("cart")
        data['cart_total'] = redis.hlen(f"cart_{user.id}")

        return data


def get_user_by_account(account):
    """"
    根据账号信息获取user模型实例对象
    :param account: 账号信息， 可以是用户名，也可以是手机号，或者其他可用于识别身份的字段信息
    :return: User对象 或者None
    """
    user = UserModel.objects.filter(Q(mobile=account) | Q(username=account) | Q(email=account)).first()
    return user


class CustomAuthBackend(ModelBackend):
    """
    自定义用户认证类[实现多条件登录]
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        多条件认证方法
        :param request: 本次客户端的http请求对象
        :param username: 本次客户端提交的用户信息， 可以是username， mobile或者其他的唯一字段
        :param password: 本次客户端提交的用户密码
        :param kwargs: 额外参数
        :return : 返回用户
        """
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        # 根据用户名信息username获取账户信息
        user = get_user_by_account(username)
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
