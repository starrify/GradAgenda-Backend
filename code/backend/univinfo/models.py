from django.db import models

class Semester(models.Model):
	name = models.CharField(max_length=20)
	start = models.DateField()
	end = models.DateField()

	def __unicode__(self):
		return self.name

class University(models.Model):
	name = models.CharField(max_length=50)
	shortname = models.CharField(max_length=20)
	address = models.CharField(max_length=100)
	numofsemesters = models.PositiveIntegerField()
	semester = models.ManyToManyField(Semester)
	description = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

class Major(models.Model):
	name = models.CharField(max_length=50)
	shortname = models.CharField(max_length=30)

	def __unicode__(self):
		return self.name

class Professor(models.Model):
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	uid = models.CharField(max_length=20)
	title = models.CharField(max_length=20)
	prefix = models.CharField(max_length=10)
	gender = models.CharField(max_length=10)
	image = models.CharField(max_length=255, blank=True, null=True)
	university = models.ForeignKey(University)
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
	semester = models.ForeignKey(Semester)
	weekday = models.CharField(max_length=10)
	starttime = models.TimeField()
	endtime = models.TimeField()
	location = models.CharField(max_length=100)

	def __unicode__(self):
		return u'%s\'s office hour on %s' % (self.professor, self.weekday)

class Course(models.Model):
	name = models.CharField(max_length=50)
	number = models.CharField(max_length=30)
	major = models.ManyToManyField(Major)
	
	def __unicode__(self):
		return self.name

class Section(models.Model):
	name = models.CharField(max_length=50)
	number = models.CharField(max_length=30)
	course = models.ForeignKey(Course)
	professor = models.ManyToManyField(Professor)
	description = models.CharField(max_length=200)
	rate = models.FloatField()
	ratecount = models.IntegerField()

	def __unicode__(self):
		return self.title

class Lecture(models.Model):
	section = models.ForeignKey(Section)
	semester = models.ForeignKey(Semester)
	weekday = models.CharField(max_length=10)	#extracted from $schedule
	starttime = models.TimeField()	#extracted from $schedule
	endtime = models.TimeField()	#extracted from $schedule
	location = models.CharField(max_length=100)	#extracted from $buildingName + $roomNumber
	classtype = models.SmallIntegerField() #0 lecture, 1 discussion, 2 experiment ...

	def __unicode__(self):
		if self.classtype == 0 :
			return u'Lecture of %s on %s' % (self.course, self.weekday)
		elif self.classtype == 1:
			return u'Discussion of %s on %s' % (self.course, self.weekday)
		elif self.classtype ==2:
			return u'Experiment of %s on %s' % (self.course, self.weekday)



