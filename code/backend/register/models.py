from django.db import models

# Create your models here.
class user(models.Model):
    user_name = models.CharField(max_length=20)
    user_id   = models.IntegerField(primary_key=True)
    user_password    = models.CharField(max_length=20)
    user_accounttype = models.CharField(max_length=10,null=True,blank=True)
    user_accountnum  = models.CharField(max_length=20,null=True,blank=True)
    user_email       = models.EmailField()
    user_university  = models.CharField(max_length=20,null=True,blank=True)
    user_college     = models.CharField(max_length=20,null=True,blank=True)
    user_major       = models.CharField(max_length=20,null=True,blank=True)
    user_grade       = models.CharField(max_length=20,null=True,blank=True)
    user_gender      = models.IntegerField(null=True,blank=True)

    def __unicode__(self):
        return self.user_name