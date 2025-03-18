from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django_redis import get_redis_connection

# 对日志调用
import logging
logger = logging.getLogger('django')

# Create your views here.
class HomeAPIView(APIView):
    def get(self, request):
        """测试代码， 测试完成以后将来可以删除"""
        # 测试日志功能
        # logger.error("error信息")
        # logger.info("info信息")
        redis = get_redis_connection("sms_code")
        brother = redis.lrange("brother", 0, -1)
        return Response(brother, status.HTTP_200_OK)
