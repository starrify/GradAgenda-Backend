from django.db import models

from backend.univinfo.models import University, Major

class User(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=50)
    nick_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50, default='Unknown')
    last_name = models.CharField(max_length=50, default='Unknown')
    gender = models.CharField(max_length=10, default='Unknown')
    phone = models.CharField(max_length=20, default='Unknown')
    eas_id = models.CharField(max_length=20, default='Unknown')    #educational administration system id
    tpa_type = models.CharField(max_length=10, default='Unknown')  #third part account type
    tpa_id = models.CharField(max_length=20, default='Unknown')    #third part account id
    tpa_token = models.CharField(max_length=255, default='Unknown')
    image = models.CharField(max_length=255, default='Unknown')
    university = models.ForeignKey(University)
    major = models.ForeignKey(Major)


class UserState(models.Model):
    user    = models.ForeignKey(User)
    token   = models.CharField(max_length = 64)
    ip      = models.CharField(max_length = 20)

    def __unicode__(self):
        return self.nick_name