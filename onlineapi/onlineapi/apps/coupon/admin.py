from django.contrib import admin
from .models import Coupon, CouponDirection, CouponCourseCat, CouponCourse, CouponLog


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
    """优惠券使用记录的模型管理器"""
    list_display = ["id", "user", "coupon", "order", "use_status", "use_time"]


admin.site.register(CouponLog, CouponLogModelAdmin)
