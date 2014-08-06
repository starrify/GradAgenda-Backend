from rest_framework import serializers
from backend.curriculum.models import CourseItem, Review

class CourseItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = CourseItem
		fields = (
					'user',
					'section',
					'grade',
					'status',
					)

class ReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Review
		fields = (
					'created',
					'rate',
					'comment',
					'user',
					'professor',
					'section',
					'is_course',
					)
