from rest_framework import serializers
from django.forms import widgets
from backend.personal.models import User,UserState
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'email',
                  'password',
                  'nick_name',
                  'first_name',
                  'last_name',
                  'gender',
                  'phone',
                  'tpa_type',
                  'tpa_id',
                  'tpa_token',
                  'image',
                  'university',
                  'major',
                )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'email',
                  'nick_name',
                  'first_name',
                  'last_name',
                  'gender',
                  'phone',
                  'image',
                  'university',
                  'major',
                )

class UserStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserState
        fields = (
              'user',
              'token',
              'ip',
          )