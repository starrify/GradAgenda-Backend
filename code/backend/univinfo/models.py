from django.db import models

class University(models.Model):
	shortname = models.CharField(max_length=30)
	fullname = models.CharField(max_length=60)	

	def __unicode__(self):
		return self.fullname

class Major(models.Model):
	shortname = models.CharField(max_length=30)
	fullname = models.CharField(max_length=60)
	
	def __unicode__(self):
		return self.name

class Semester(models.Model):
	name = models.CharField(max_length=20)
	university = models.ForeignKey(University)
	start = models.DateField()
	end = models.DateField()

class Professor(models.Model):
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	title = models.CharField(max_length=20, default='Unknown')
	gender = models.CharField(max_length=10, default='Unknown')
	image = models.CharField(max_length=255, default='Unknown')
	university = models.ForeignKey(University)
	email = models.CharField(max_length=100, default='Unknown')
	phone = models.CharField(max_length=20, default='Unknown')
	office = models.CharField(max_length=100, default='Unknown')
	description = models.CharField(max_length=200, default='Unknown')
	rate = models.FloatField(default=0.0)
	ratecount = models.IntegerField(default=0)
	def __unicode__(self):
		return u'%s %s' % (self.prefix, self.last_name)

#class OfficeHour(models.Model):
#	professor = models.ForeignKey(Professor)
#	weekday = models.CharField(max_length=10)
#	starttime = models.TimeField()
#	endtime = models.TimeField()
#	location = models.CharField(max_length=100)

#	def __unicode__(self):
#		return u'%s\'s office hour on %s' % (self.professor, self.weekday)

class Course(models.Model):
	fullname = models.CharField(max_length=60)
	shortname = models.CharField(max_length=30)
	university = models.ForeignKey(University)
	department = models.CharField(max_length=30)
	
	def __unicode__(self):
		return self.name

class Section(models.Model):
	name = models.CharField(max_length=30)
	semester = models.ForeignKey(Semester)
	course = models.ForeignKey(Course)
	professor = models.ManyToManyField(Professor)
	start = models.DateField()
	end = models.DateField()
	description = models.CharField(max_length=200, default='Unknown')
	rate = models.FloatField(default=0.0)
	ratecount = models.IntegerField(default=0)

	def __unicode__(self):
		return self.name

class Lecture(models.Model):
	section = models.ForeignKey(Section)
	weekday = models.SmallIntegerField()	#extracted from $schedule
	starttime = models.TimeField()	#extracted from $schedule
	endtime = models.TimeField()	#extracted from $schedule
	location = models.CharField(max_length=100)	#extracted from $buildingName + $roomNumber

	def __unicode__(self):
		return u'Lecture of %s on %s' % (self.course, self.weekday)




