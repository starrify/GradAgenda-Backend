from django.db import models

from backend.personal.models import User
from backend.univinfo.models import Section, Professor

class CourseItem(models.Model):
	user = models.ForeignKey(User)
	section = models.ForeignKey(Section)
	grade = models.CharField(max_length=10, default='Unknown')
	status = models.SmallIntegerField(default=1)
	#0 for registered, 1 for selected, 2 for rejected, 3 for passed, 4 for failed
	def __unicode__(self):
		return u'%s in course %s' % (self.user, self.course)

class Review(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	rate = models.FloatField()
	comment = models.CharField(max_length=200)
	user = models.ForeignKey(User)
	professor = models.ForeignKey(Professor, blank=True, null=True)
	section = models.ForeignKey(Section, blank=True, null=True)
	is_course = models.BooleanField()	#is this review for section or professor

	def __unicode__(self):
		if self.is_course :
			return u'%s\'s review for course %s' % (self.user, self.course)
		else :
			return u'%s\'s review for %s' % (self.course, self.professor)
