import re, constants
from rest_framework import serializers

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from .models import User
from tencentcloudapi import TencentCloudAPI, TencentCloudSDKException

from django_redis import get_redis_connection


class UserRegisterModelSerializer(serializers.ModelSerializer):
    """
    用户注册的序列化器
    """
    re_password = serializers.CharField(required=True, write_only=True)
    sms_code = serializers.CharField(min_length=4, max_length=6, required=True, write_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    ticket = serializers.CharField(required=True, write_only=True, help_text="滑块验证码的临时凭证")
    randstr = serializers.CharField(required=True, write_only=True, help_text="滑块验证码的随机字符串")

    class Meta:
        model = User
        fields = ["mobile", "password", "re_password", "sms_code", "access_token", "refresh_token", "ticket", "randstr", ]
        extra_kwargs = {
            "mobile": {
                "required": True, "write_only": True
            },
            "password": {
                "required": True, "write_only": True, "min_length": 6, "max_length": 16
            },
        }

    def validate(self, data):
        """验证客户端数据"""
        # 手机号格式验证
        mobile = data.get("mobile", None)
        if not re.match("^1[3-9]\\d{9}$", mobile):
            raise serializers.ValidationError(detail="手机号格式不正确", code="mobile")
        # 密码和确认密码
        password = data.get("password")
        re_password = data.get("re_password")
        if password != re_password:
            raise serializers.ValidationError(detail="两次密码不一致", code="password")
        # 手机号是否注册过
        try:
            user = User.objects.get(mobile=mobile)
            raise serializers.ValidationError(detail="手机号已注册")
        except User.DoesNotExist:
            pass
        # todo 防水墙验证码
        # api = TencentCloudAPI()
        # result = api.captcha(
        #     data.get("ticket"),
        #     data.get("randstr"),
        #     self.context['request']._request.META.get("REMOTE_ADDR")  # 客户端IP
        # )
        # if not result:
        #     raise serializers.ValidationError(detail="滑块验证码校验失败！")
        # todo 验证短信验证码
        # 从redis中提取短信
        redis = get_redis_connection("sms_code")
        code = redis.get(f"sms_{mobile}")
        if code is None:
            """获取不到验证码，则表示验证码已经过期了"""
            raise serializers.ValidationError(detail="短信验证码已过期", code="sms_code")
        # 从redis提取的数据，字符串都是bytes类型，所以decode
        if code.decode() != data.get("sms_code"):
            raise serializers.ValidationError(detail="短信验证码错误", code="sms_code")
        print(f"code={code.decode()}, sms_code={data.get('sms_code')}")
        # 删除掉redis中的短信，后续不管用户是否注册成功，至少当前这条短信验证码已经没有用处了
        redis.delete(f"sms_{mobile}")
        return data

    def create(self, validated_data):
        """
        保存用户信息，完成注册
        """
        mobile = validated_data.get("mobile")
        password = validated_data.get("password")

        user = User.objects.create_user(
            mobile=mobile,
            password=password,
            username=mobile,
            avatar=constants.DEFAULT_USER_AVATAR,
        )

        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # 新增JWT令牌生成逻辑
        from authenticate import CustomTokenObtainPairSerializer
        custom_token = CustomTokenObtainPairSerializer()
        token_data = custom_token.generate_jwt_tokens(instance)
        data.update(token_data)
        return data
