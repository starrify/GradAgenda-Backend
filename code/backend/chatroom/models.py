from django.db import models
from backend.personal.models import User


class Chatroom(models.Model):
	name = models.CharField(max_length=50)
	membercount = models.IntegerField()
	messagecount = models.IntegerField()
	surveycount = models.IntegerField()
	member = models.ManyToManyField(User)

	def __unicode__(self):
		return self.name

class Message(models.Model):
	content = models.CharField(max_length=200)
	chatroom = models.ForeignKey(Chatroom)
	sender = models.ForeignKey(User)
	time = models.DateTimeField()
	is_survey = models.BooleanField()
	
	def __unicode__(self):
		if is_survey :
			return u'Survey: %s' % (self.content)
		else :
			return u'Message: %s' % (self,content)


class Timespan(models.Model):
	survey = models.ForeignKey(Message)
	startdatetime = models.DateTimeField()
	enddatetime = models.DateTimeField(blank=True, null=True)
	raise_user = models.ManyToManyField(User)
	agree_user = models.ManyToManyField(User, blank=True, null=True)
	disagree_user = models.ManyToManyField(User, blank=True, null=True)

	def __unicode__(self):
		return u'Timespan of %s' % (self.survey)

