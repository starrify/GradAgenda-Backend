from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    nick_name = models.CharField(max_length=20) 
    password = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    image = models.ImageField(upload_to='images', max_length=255, blank=True, null=True)
    eas_id = models.CharField(max_length=20, blank=True)    #educational administration system id
    tpa_type = models.CharField(max_length=10, blank=True)  #third part account type
    tpa_id = models.CharField(max_length=20, blank=True)    #third part account id
    university = models.ForeignKey(University)
    college = models.ManyToManyField(College)
    major = models.ManyToManyField(Major)
    grade = models.ForeignKey(Grade)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)

    def __unicode__(self):
        return self.nick_name

class University(models.Model):
	name = models.CharField(max_length=50)
	address = models.CharField(max_length=100)
	semester = models.PositiveIntegerField()

	def __unicode__(self):
		return self.name

class College(models.Model):
	name = models.CharField(max_length=50)
	university = ForeignKey(University)

	def __unicode__(self):
		return self.name

class Major(models.Model):
	name = models.CharField(max_length=50)
	college = ManyToManyField(College)

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
    university = ForeignKey(University)
    college = models.ManyToManyField(College)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    office = models.CharField(max_length=100)
    description = models.CharField(max_lenth=200)
    rate = models.FloatField()
	ratecount = models.IntegerField()
	def __unicode__(self):
		return u'%s %s' % (self.prefix, self.last_name)

class Officehour(models.Model):
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
	professor = models.ManyToManyField(Professor)
	description = models.CharField(max_lenth=200)
	rate = models.FloatField()
	ratecount = models.IntegerField()
	user = models.ManyToManyField(User)

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

class Event(models.Model):
	name = models.CharField(max_length=50)
	startdatetime = models.DateTimeField()
	enddatetime = models.DateTimeField()
	location = models.CharField(max_length=100)
	is_private = models.BooleanField()
	user = models.ManyToManyField(User)

	def __unicode__(self):
		if self.is_private :
			return u'Private event of %s - %s' % (self.user, self.name)
		else :
			return u'Public event - %s' % (self.name)


class Review(models.Model):
	rate = models.FloatField()
	text = models.CharField(max_length=200)
	user = models.ForeignKey(User)
	professor = ForeignKey(Professor)
	course = ForeignKey(Course)
	flag = models.SmallPositiveInteger()	#0 for professor, 1 for course, 2 for event

	def __unicode__(self):
		if self.is_course :
			return u'%s\'s review for course %s' % (self.user, self.course)
		else :
			return u'%s\'s review for %s' % (self.course, self.professor)

class Friendship(models.Model):
	user1 = models.ForeignKey(User)
	user2 = models.ForeignKey(User)

	def __unicode__(self):
		return u'Friendship between %s and %s' % (self.user1, self.user2)

class Friendrequest(models.Model):
	sender = models.ForeignKey(User)
	receiver = models.ForeignKey(User)
	status = models.SmallPositiveInteger()	#0 for sent, 1 for accepted, 2 for rejected

	def __unicode__(self):
		return u'Friend Request from %s to %s, status: %d' % (self.sender, self.receiver, self.status)

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
	raise_user = ManyToManyField(User)
	agree_user = models.ManyToManyField(User, blank=True, null=True)
	disagree_user = models.ManyToManyField(User, blank=True, null=True)

	def __unicode__(self):
		return u'Timespan of %s' % (self.survey)



