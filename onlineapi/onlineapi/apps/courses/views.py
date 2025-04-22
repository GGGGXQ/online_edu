from rest_framework.generics import ListAPIView

from .models import CourseDirection, CourseCategory
from .serializers import CourseDirectionModelSerializer, CourseCategoryModelSerializer


# Create your views here.
class CourseDirectionListAPIView(ListAPIView):
    """学习方向"""
    queryset = CourseDirection.objects.filter(is_show=True, is_deleted=False).order_by("orders", "-id")
    serializer_class = CourseDirectionModelSerializer
    pagination_class = None


class CourseCategoryListAPIView(ListAPIView):
    """学习分类"""
    serializer_class = CourseCategoryModelSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = CourseCategory.objects.filter(is_show=True, is_deleted=False)
        direction = int(self.kwargs.get("direction"), 0)
        if direction > 0:
            queryset = queryset.filter(direction=direction)
        return queryset.order_by("orders", "-id").all()
