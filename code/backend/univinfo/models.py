from django.db import models

class University(models.Model):
	name = models.CharField(max_length=50)
	shortname = models.CharField(max_length=20)
	address = models.CharField(max_length=100, default='')
	description = models.CharField(max_length=200, default='')

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
	uid = models.CharField(max_length=20, default='')
	title = models.CharField(max_length=20, default='')
	prefix = models.CharField(max_length=10, default='')
	gender = models.CharField(max_length=10, default='')
	image = models.CharField(max_length=255, default='')
	university = models.ForeignKey(University, default='Unknown')
	email = models.EmailField(blank=True, null=True)
	phone = models.CharField(max_length=20, default='')
	office = models.CharField(max_length=100, default='')
	description = models.CharField(max_length=200, default='')
	rate = models.FloatField(default=0)
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
	name = models.CharField(max_length=50)
	number = models.CharField(max_length=30)
	major = models.ManyToManyField(Major, default='Unknown')
	
	def __unicode__(self):
		return self.name

class Section(models.Model):
	name = models.CharField(max_length=50)
	number = models.CharField(max_length=30)
	course = models.ForeignKey(Course)
	professor = models.ManyToManyField(Professor)
	start = models.DateField()
	end = models.DateField()
	description = models.CharField(max_length=200, default='')
	rate = models.FloatField()
	ratecount = models.IntegerField()

	def __unicode__(self):
		return self.title

class Lecture(models.Model):
	section = models.ForeignKey(Section)
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



