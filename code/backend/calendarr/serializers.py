from rest_framework import serializers
from backend.calendarr.models import EventItem

class EventSerializer(serializers.ModelSerializer):
	class Meta:
		model = EventItem
		fields = ('id', 
				  'user', 
				  'name', 
				  'startdatetime', 
				  'location',
				  'status',
				  )

