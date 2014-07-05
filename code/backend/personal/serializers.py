from rest_framework import serializers
from django.forms import widgets
from backend.personal.models import User
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
                  'grade',
                  'email',
                  'phone',
                )
