from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django_redis import get_redis_connection
from rest_framework.generics import ListAPIView

from .models import Nav
from .serializers import NavModelSerializer

import constants

# 对日志调用
import logging

logger = logging.getLogger('django')


# Create your views here.
class NavHeaderListAPIView(ListAPIView):
    serializer_class = NavModelSerializer
    queryset = Nav.objects.filter(position=constants.NAV_HEADER_POSITION, is_show=True, is_deleted=False).ordered_by('orders', '-id')[:constants.NAV_HEADER_SIZE]


class NavFooterListAPIView(ListAPIView):
    serializer_class = NavModelSerializer
    queryset = Nav.objects.filter(position=constants.NAV_FOOTER_POSITION, is_show=True, is_deleted=False).ordered_by('orders', '-id')[:constants.NAV_FOOTER_SIZE]
