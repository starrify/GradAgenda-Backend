from rest_framework import serializers
from django.forms import widgets
from backend.personal.models import User,UserState
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'nick_name',
                  'password',
                  'gender',
                  'image',
                  'eas_id',
                  'tpa_type',
                  'tpa_id',
                  'university',
                  'email',
                  'phone',
                )

class UserStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserState
        fields = (
              'user',
              'token',
              'ip',
          )