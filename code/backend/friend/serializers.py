from rest_framework import serializers
from backend.friend.models import FriendRelation, FriendRequest

class RelationSerializer(serializers.ModelSerializer):
	class Meta:
		model = FriendRelation
		fields = ('id',
				  'user1',
				  'user2',			  
				  )


class RequestSerializer(serializers.ModelSerializer):
	class Meta:
		model = FriendRequest
		fields = ('id',
				  'created',
				  'sender',
				  'receiver',
				  )