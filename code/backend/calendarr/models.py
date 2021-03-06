from django.db import models
# Create your models here.

from backend.personal.models import User

class EventItem(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=100, default='Unknown')
	startdatetime = models.DateTimeField()
	location = models.CharField(max_length=100, default='Unknown')
	status = models.SmallIntegerField(default=0) 
	#0 for normal, 1 for urgent
	def __unicode__(self):
		return u'%s in event %s' % (self.user, self.event)

	class Meta:
		ordering = ('startdatetime',)