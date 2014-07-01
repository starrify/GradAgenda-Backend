from django.db import models

from backend.personal.models import User

class FriendRelation(models.Model):
	user_1 = models.ForeignKey(User)
	user_2 = models.ForeignKey(User)

	def __unicode__(self):
		return u'Friendship between %s and %s' % (self.user1, self.user2)

class FriendRequest(models.Model):
	sender = models.ForeignKey(User)
	receiver = models.ForeignKey(User)
	status = models.SmallIntegerField()	#0 for sent, 1 for accepted, 2 for rejected

	def __unicode__(self):
		return u'Friend Request from %s to %s, status: %d' % (self.sender, self.receiver, self.status)