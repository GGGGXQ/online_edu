from django.contrib import admin
from django.utils.timezone import datetime
from django_redis import get_redis_connection

import json

from .models import Coupon, CouponDirection, CouponCourseCat, CouponCourse, CouponLog
from .services import add_coupon_to_redis


# Register your models here.
class CouponDirectionInline(admin.TabularInline):
    """学习方向的内嵌类"""
    model = CouponDirection
    fields = ["id", "direction"]


class CouponCourseCatInline(admin.TabularInline):
    """课程分类的内嵌类"""
    model = CouponCourseCat
    fields = ["id", "category"]


class CouponCourseInline(admin.TabularInline):
    """课程的内嵌类"""
    model = CouponCourse
    fields = ["id", "course"]


class CouponModelAdmin(admin.ModelAdmin):
    """优惠券的模型管理器"""
    list_display = ["id", "name", "start_time", "end_time", "total", "has_total", "coupon_type", "get_type"]
    inlines = [CouponDirectionInline, CouponCourseCatInline, CouponCourseInline]


admin.site.register(Coupon, CouponModelAdmin)


class CouponLogModelAdmin(admin.ModelAdmin):
    """优惠券优惠券发放和使用记录"""
    list_display = ["id", "user", "coupon", "order", "use_status", "use_time"]

    def save_model(self, request, obj, form, change):
        """
        保存或更新记录时自动执行的钩子
        request: 本次客户端提交的请求对象
        obj: 本次操作的模型实例对象
        form: 本次客户端提交的表单数据
        change: 值为True,表示更新数据，值为False，表示添加数据
        """
        obj.save()
        redis = get_redis_connection("coupon")
        if obj.use_status == 0 and obj.use_time is None:
            # 记录优惠券信息到redis中
            add_coupon_to_redis(obj)
        else:
            redis.delete(f"{obj.user.id}:{obj.id}")

    def delete_model(self, request, obj):
        """
        删除记录时自动执行的钩子
        request: 本次客户端提交的请求对象
        obj: 本次操作的模型
        """
        print(obj, "详情页中删除一个记录")
        redis = get_redis_connection("coupon")
        redis.delete(f"{obj.user.id}:{obj.id}")
        obj.delete()

    def delete_queryset(self, request, queryset):
        """在列表页中进行删除优惠券记录时，也要同步删除容redis中的记录"""
        print(queryset, "列表页中删除多个记录")
        redis = get_redis_connection("coupon")
        for obj in queryset:
            redis.delete(f"{obj.user.id}:{obj.id}")
        queryset.delete()


admin.site.register(CouponLog, CouponLogModelAdmin)
