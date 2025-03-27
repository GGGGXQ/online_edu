from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView


from authenticate import CustomTokenObtainPairSerializer


# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
