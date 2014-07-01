from django.db import models
#from backend.personal.models import User

class University(models.Model):
	name = models.CharField(max_length=50)
	address = models.CharField(max_length=100)
	semester = models.PositiveIntegerField()

	def __unicode__(self):
		return self.name

class College(models.Model):
	name = models.CharField(max_length=50)
	university = models.ForeignKey(University)

	def __unicode__(self):
		return self.name

class Major(models.Model):
	name = models.CharField(max_length=50)
	college = models.ManyToManyField(College)

	def __unicode__(self):
		return self.name

class Grade(models.Model):
	name = models.CharField(max_length=20)

	def __unicode__(self):
		return self.name

class Professor(models.Model):
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	title = models.CharField(max_length=20)
	prefix = models.CharField(max_length=10)
	gender = models.CharField(max_length=10)
	image = models.ImageField(upload_to='images', max_length=255, blank=True, null=True)
	university = models.ForeignKey(University)
	college = models.ManyToManyField(College)
	email = models.EmailField(blank=True, null=True)
	phone = models.CharField(max_length=20, blank=True)
	office = models.CharField(max_length=100)
	description = models.CharField(max_length=200)
	rate = models.FloatField()
	ratecount = models.IntegerField()
	def __unicode__(self):
		return u'%s %s' % (self.prefix, self.last_name)

class OfficeHour(models.Model):
	professor = models.ForeignKey(Professor)
	weekday = models.CharField(max_length=10)
	starttime = models.TimeField()
	endtime = models.TimeField()
	location = models.CharField(max_length=100)

	def __unicode__(self):
		return u'%s\'s office hour on %s' % (self.professor, self.weekday)

class Course(models.Model):
	name = models.CharField(max_length=50)
	number = models.CharField(max_length=50)
	college = models.ManyToManyField(College)
	major = models.ManyToManyField(Major)
	grade = models.ManyToManyField(Grade)
	professor = models.ManyToManyField(Professor)
	description = models.CharField(max_length=200)
	rate = models.FloatField()
	ratecount = models.IntegerField()

	def __unicode__(self):
		return self.name

class Lecture(models.Model):
	course = models.ForeignKey(Course)
	weekday = models.CharField(max_length=10)
	starttime = models.TimeField()
	endtime = models.TimeField()
	location = models.CharField(max_length=100)
	is_discussion = models.BooleanField()

	def __unicode__(self):
		if self.is_discussion :
			return u'Discussion of %s on %s' % (self.course, self.weekday)
		else :
			return u'Lecture of %s on %s' % (self.course, self.weekday)



