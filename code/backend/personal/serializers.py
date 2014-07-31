from rest_framework import serializers
from django.forms import widgets
from backend.personal.models import User,UserState
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',
                  'password',
                  'nick_name',
                  'first_name',
                  'last_name',
                  'gender',
                  'phone',
                  'eas_id',
                  'tpa_type',
                  'tpa_id',
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