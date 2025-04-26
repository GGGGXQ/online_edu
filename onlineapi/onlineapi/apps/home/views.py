from .models import Nav, Banner
from .serializers import NavModelSerializer, BannerModelSerializer

import constants
from views import CacheListAPIView


# Create your views here.
class NavHeaderListAPIView(CacheListAPIView):
    serializer_class = NavModelSerializer
    queryset = Nav.objects.filter(position=constants.NAV_HEADER_POSITION, is_show=True, is_deleted=False).order_by('orders', '-id')[:constants.NAV_HEADER_SIZE]


class NavFooterListAPIView(CacheListAPIView):
    serializer_class = NavModelSerializer
    queryset = Nav.objects.filter(position=constants.NAV_FOOTER_POSITION, is_show=True, is_deleted=False).order_by('orders', '-id')[:constants.NAV_FOOTER_SIZE]


class BannerListAPIView(CacheListAPIView):
    """轮播广告视图"""
    serializer_class = BannerModelSerializer
    queryset = Banner.objects.filter(is_show=True, is_deleted=False).order_by('orders', '-id')[:constants.BANNER_SIZE]
