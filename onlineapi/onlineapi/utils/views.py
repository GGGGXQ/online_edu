import constants
from rest_framework.generics import ListAPIView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class CacheListAPIView(ListAPIView):
    """列表缓存视图"""
    @method_decorator(cache_page(constants.LIST_PAGE_CACHE_TIME))
    def get(self, request, *args, **kwargs):
        # 重写ListAPIView的get方法，但是不改动源代码。仅仅装饰而已
        return super().get(request, *args, **kwargs)