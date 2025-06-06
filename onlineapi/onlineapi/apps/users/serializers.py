import constants
import re
import logging
from rest_framework import serializers

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from .models import User, UserCourse
from tencentcloudapi import TencentCloudAPI, TencentCloudSDKException

from django_redis import get_redis_connection


logger = logging.getLogger("django")


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

        try:
            # 避免循环依赖的动态导入（若存在循环依赖问题）
            from authenticate import CustomTokenObtainPairSerializer
            custom_token = CustomTokenObtainPairSerializer()

            # 生成JWT令牌（修正方法名，假设使用标准 get_token）
            token_pair = custom_token.get_token(instance)
            token_data = {
                'access_token': str(token_pair.access),
                'refresh_token': str(token_pair),
            }
            data.update(token_data)
        except (ImportError, AttributeError) as e:
            logger.error(f"JWT Token generation failed: {str(e)}", exc_info=True)
            raise serializers.ValidationError("Failed to generate authentication tokens")
        except Exception as e:
            logger.critical(f"Unexpected error in JWT generation: {str(e)}", exc_info=True)
            raise serializers.ValidationError("Internal server error")

        return data


class UserCourseModelSerializer(serializers.ModelSerializer):
    """用户课程信息序列化器"""
    course_cover = serializers.ImageField(source="course.course_cover")
    course_name = serializers.CharField(source="course.name")
    chapter_name = serializers.CharField(source="chapter.name", default="")
    chapter_id = serializers.IntegerField(source="chapter.id", default=0)
    chapter_orders = serializers.IntegerField(source="chapter.orders", default=0)
    lesson_id = serializers.IntegerField(source="lesson.id", default=0)
    lesson_name = serializers.CharField(source="lesson.name", default="")
    lesson_orders = serializers.IntegerField(source="lesson.orders", default=0)
    course_type = serializers.IntegerField(source="course.course_type", default=0)
    get_course_type_display = serializers.CharField(source="course.get_course_type_display",default="")

    class Meta:
        model = UserCourse
        fields = [
            "course_id", "course_cover",  "course_name", "study_time",
            "chapter_id", "chapter_orders", "chapter_name",
            "lesson_id", "lesson_orders", "lesson_name",
            "course_type", "get_course_type_display", "progress",
            "note", "qa", "code"
        ]
