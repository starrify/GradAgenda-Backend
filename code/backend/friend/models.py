from django.db import models

from backend.personal.models import User

class FriendRelation(models.Model):
	user1 = models.ForeignKey(User, related_name='User1')
	user2 = models.ForeignKey(User, related_name='User2')

	def __unicode__(self):
		return u'Friendship between %s and %s' % (self.user1, self.user2)

class FriendRequest(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	sender = models.ForeignKey(User, related_name='Sender')
	receiver = models.ForeignKey(User, related_name='Receiver')
#	status = models.SmallIntegerField()	#0 for sent, 1 for accepted, 2 for rejected

	def __unicode__(self):
		return u'Friend Request from %s to %s, status: %d' % (self.sender, self.receiver, self.status)

	class Meta:
		ordering = ('-created',)