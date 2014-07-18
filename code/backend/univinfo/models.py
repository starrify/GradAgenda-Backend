from django.db import models

class University(models.Model):
	name = models.CharField(max_length=50)
	shortname = models.CharField(max_length=20)
	address = models.CharField(max_length=100)
	semester = models.PositiveIntegerField()

	def __unicode__(self):
		return self.name

class College(models.Model):
	name = models.CharField(max_length=50)
	university = models.ForeignKey(University)

	def __unicode__(self):
		return self.name

class Department(models.Model):
	name = models.CharField(max_length=50)
	college = models.ForeignKey(College)

	def __unicode__(self):
		return self.name

class Major(models.Model):
	name = models.CharField(max_length=50)
	department = models.ManyToManyField(Department)

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
	title = models.CharField(max_length=50)		#title
	semester = models.CharField(max_length=20)	#termYear+'whatever makes it unique'(perhaps from course_id)
	code = models.CharField(max_length=50)		#course_code
	catalog = models.CharField(max_length=20, blank=True, null=True)	#courseCatalog
	section = models.CharField(max_length=20)	#section_label
	department = models.ManyToManyField(Department)		#dept_desc	
	instructor = models.ManyToManyField(Professor)	#instructor
	unit = models.FloatField()	#unit
	description = models.CharField(max_length=200) #some other information dependent on specific universities
	rate = models.FloatField()
	ratecount = models.IntegerField()

	def __unicode__(self):
		return self.title

class Class(models.Model):   #Changed from Lecture
	course = models.ForeignKey(Course)
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



