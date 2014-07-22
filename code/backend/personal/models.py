from django.db import models

from backend.univinfo.models import University, Major

class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    nick_name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    image = models.CharField(max_length=255, blank=True, null=True)
    eas_id = models.CharField(max_length=20, blank=True)    #educational administration system id
    tpa_type = models.CharField(max_length=10, blank=True)  #third part account type
    tpa_id = models.CharField(max_length=20, blank=True)    #third part account id
    university = models.ForeignKey(University)
    major = models.ManyToManyField(Major)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)

class UserState(models.Model):
    user    = models.ForeignKey(User)
    token   = models.CharField(max_length = 64)
    ip      = models.CharField(max_length = 20)

    def __unicode__(self):
        return self.nick_name