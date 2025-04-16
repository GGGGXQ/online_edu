import re, constants

from rest_framework import serializers
from rest_framework_simplejwt.settings import api_settings

from .models import User
from tencentcloudapi import TencentCloudAPI, TencentCloudSDKException


class UserRegisterModelSerializer(serializers.ModelSerializer):
    """
    用户注册的序列化器
    """
    re_password = serializers.CharField(required=True, write_only=True)
    sms_code = serializers.CharField(min_length=4, max_length=6, required=True, write_only=True)
    token = serializers.CharField(read_only=True)
    ticket = serializers.CharField(required=True, write_only=True, help_text="滑块验证码的临时凭证")
    randstr = serializers.CharField(required=True, write_only=True, help_text="滑块验证码的随机字符串")

    class Meta:
        model = User
        fields = ["mobile",  "password", "re_password", "sms_code", "token"]
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
        if not re.match("^1[3-9]\d{9}$", mobile):
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
        api = TencentCloudAPI()
        result = api.captcha(
            data.get("ticket"),
            data.get("randstr"),
            self.context['request']._requset.META.get("REMOTE_ADDR") # 客户端IP
        )
        if not result:
            raise serializers.ValidationError(data="滑块验证码校验失败！")
        # todo 验证短信验证码

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

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)

        return user
