from django.urls import path, re_path

from . import views

urlpatterns = [
    # 登录视图，获取access_token和refresh_token
    path("login/", views.LoginAPIView.as_view(), name="login"),
    re_path(r"^mobile/(?P<mobile>1[3-9]\d{9})/$", views.MobileAPIView.as_view()),
    path("register/", views.UserAPIView.as_view()),
    re_path(r"^sms/(?P<mobile>1[3-9]\d{9})/$", views.SMSAPIView.as_view()),
    path("course/", views.CourseListAPIView.as_view()),
]
