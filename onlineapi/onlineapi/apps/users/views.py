from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.views import APIView, Response, status
from rest_framework.generics import CreateAPIView, ListAPIView
# from tencentcloud.common.exception import TencentCloudSDKException
from django.core.exceptions import ObjectDoesNotExist

from authenticate import CustomTokenObtainPairSerializer
# from tencentcloudapi import TencentCloudAPI

from .models import User, UserCourse
from .serializers import UserRegisterModelSerializer, UserCourseModelSerializer
from .tasks import send_sms

from courses.paginations import CourseListPageNumberPagination
from courses.models import Course

# 短信模块
import random
from django_redis import get_redis_connection
from django.conf import settings
# from ronglianyunapi import send_sms


# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class MobileAPIView(APIView):
    def get(self, request, mobile):
        """
        校验手机号是否注册
        :param request:
        :param mobile: 手机号
        :return:
        """
        try:
            user = User.objects.get(mobile=mobile)
            return Response({"message": "当前手机号已注册"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "ok"}, status=status.HTTP_200_OK)


class UserAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterModelSerializer


class LoginAPIView(TokenObtainPairView):
    """用户登录视图"""

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except InvalidToken as e:
            # 捕获密码错误或用户不存在的情况
            return Response({"errmsg": "用户名或密码错误"}, status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            return Response({"errmsg": "用户不存在"}, status=status.HTTP_404_NOT_FOUND)
        # # 校验用户操作验证码成功以后的ticket临时票据
        # try:
        #     api = TencentCloudAPI()
        #     result = api.captcha(
        #         request.data.get("ticket"),
        #         request.data.get("randstr"),
        #         request._request.META.get("REMOTE_ADDR"),
        #     )
        #     if result:
        #         # 验证通过
        #         print("验证通过")
        #         # 登录实现代码，调用父类实现的登录视图方法
        #         return super().post(request, *args, **kwargs)
        #     else:
        #         # 如果返回值不是True，则表示验证失败
        #         raise TencentCloudSDKException
        # except TencentCloudSDKException as err:
        #     return Response({"errmsg": "验证码校验失败！"}, status=status.HTTP_400_BAD_REQUEST)


# 短信模块
# /users/sms/(?P<mobile>1[3-9]\d{9})
class SMSAPIView(APIView):
    """sms短信接口视图"""

    def get(self, request, mobile):
        """发送短信验证码"""
        redis = get_redis_connection("sms_code")
        # 判断手机短信是否处于发送冷却中[60秒只能发送一条]
        interval = redis.ttl(f"interval_{mobile}")  # 通过ttl方法可以获取保存在redis中的变量的剩余有效期
        if interval != -2:
            return Response({"errmsg": f"短信发送过于频繁，请{interval}秒后再次点击获取!"}, status=status.HTTP_400_BAD_REQUEST)

        # 基于随机数生成短信验证码
        # code = "%06d" % random.randint(0, 9999)
        code = f"{random.randint(0, 9999):04d}"
        # 获取短信有效期的时间
        time = settings.RONGLIANYUN.get("sms_expire")
        # 短信发送间隔时间
        sms_interval = settings.RONGLIANYUN["sms_interval"]
        # 调用第三方sdk发送短信
        # send_sms(settings.RONGLIANYUN.get("reg_tid"), mobile, datas=(code, time // 60))
        # 异步发送短信
        send_sms.delay(settings.RONGLIANYUN.get("reg_tid"), mobile, datas=(code, time // 60))

        # 记录code到redis中，并以time作为有效期
        # 使用redis提供的管道对象pipeline来优化redis的写入操作[添加/修改/删除]
        pipe = redis.pipeline()
        pipe.multi()  # 开启事务
        pipe.setex(f"sms_{mobile}", time, code)
        pipe.setex(f"interval_{mobile}", sms_interval, "_")
        pipe.execute()  # 提交事务，同时把暂存在pipeline的数据一次性提交给redis

        return Response({"errmsg": "OK"}, status=status.HTTP_200_OK)


class CourseListAPIView(ListAPIView):
    """当前用户的课程列表信息"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserCourseModelSerializer
    pagination_class = CourseListPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        query = UserCourse.objects.filter(user=user)
        course_type = int(self.request.query_params.get("type", -1))
        course_type_list = [item[0] for item in Course.COURSE_TYPE]
        if course_type in course_type_list:
            query = query.filter(course__course_type=course_type)
        return query.order_by("-id").all()
