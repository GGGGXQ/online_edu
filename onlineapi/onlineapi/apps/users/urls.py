from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views

urlpatterns = [
    # 登录视图，获取access_token和refresh_token
    path("login/", TokenObtainPairView.as_view(), name="login"),
    # 可选：刷新token视图，使用refresh_token生成新的access_token
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # 可选：验证现有的access_token是否有效
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
