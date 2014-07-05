from django.db import models
# Create your models here.

from backend.personal.models import User

class EventItem(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=50)
	startdatetime = models.DateTimeField()
	enddatetime = models.DateTimeField()
	location = models.CharField(max_length=100)
	status = models.SmallIntegerField() 
	#0 for normal, 1 for urgent, 2 for past
	def __unicode__(self):
		return u'%s in event %s' % (self.user, self.event)
