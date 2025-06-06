"""onlineapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.views.static import serve  # 静态文件代理访问模块
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'uploads/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
    path('home/', include("home.urls")),
    path('users/', include("users.urls")),
    path('courses/', include("courses.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('cart/', include("cart.urls")),
    path("orders/", include("orders.urls")),
    path("coupon/", include("coupon.urls")),
    path("payments/", include("payments.urls")),
]
