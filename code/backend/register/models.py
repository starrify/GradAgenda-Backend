from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    nick_name = models.CharField(max_length=20) 
    password = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    image = models.ImageField(upload_to='images', max_length=255, blank=True, null=True)
    eas_id = models.CharField(max_length=20, blank=True)    #educational administration system id
    tpa_type = models.CharField(max_length=10, blank=True)  #third part account type
    tpa_id = models.CharField(max_length=20, blank=True)    #third part account id
    university = models.ForeignKey(University)
    college = models.ManyToManyField(College)
    major = models.ManyToManyField(Major)
    grade = models.ForeignKey(Grade)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)

    def __unicode__(self):
        return self.nick_name