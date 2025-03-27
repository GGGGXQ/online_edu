from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        if hasattr(user, 'avatar'):
            token['avatar'] = user.avatar.url if user.avatar else ""
        if hasattr(user, 'nickname'):
            token['nickname'] = user.nickname
        if hasattr(user, 'money'):
            token['money'] = float(user.money)
        if hasattr(user, 'credit'):
            token['credit'] = user.credit
        return token

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(request=self.context.get('request'), username=username, password=password)

        if user is None:
            raise serializers.ValidationError(
                {"detail": "No active account found with the given credentials"}
            )

        self.user = user
        refresh = self.get_token(self.user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return data
