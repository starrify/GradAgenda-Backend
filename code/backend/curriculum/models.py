from django.db import models

from backend.personal.models import User
from backend.univinfo.models import Course, Professor

class CourseItem(models.Model):
	user = models.ForeignKey(User)
	course = models.ForeignKey(Course)
	status = models.SmallIntegerField()
	#0 for registered, 1 for selected, 2 for rejected, 3 for passed, 4 for failed
	def __unicode__(self):
		return u'%s in course %s' % (self.user, self.course)

class Review(models.Model):
	rate = models.FloatField()
	comment = models.CharField(max_length=200)
	user = models.ForeignKey(User)
	professor = models.ForeignKey(Professor, blank=True, null=True)
	course = models.ForeignKey(Course, blank=True, null=True)
	is_course = models.BooleanField()

	def __unicode__(self):
		if self.is_course :
			return u'%s\'s review for course %s' % (self.user, self.course)
		else :
			return u'%s\'s review for %s' % (self.course, self.professor)
