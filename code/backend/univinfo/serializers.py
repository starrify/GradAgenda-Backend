from rest_framework import serializers
from backend.univinfo.models import University, Major, Semester, Professor, Course, Section, Lecture

class UniversitySerializer(serializers.ModelSerializer):
	class Meta:
		model = University
		fields = (
					'id',
					'shortname',
					'fullname',
					)

class MajorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Major
		fields = (
					'id',
					'shortname',
					'fullname',
					)

class SemesterSerializer(serializers.ModelSerializer):
	class Meta:
		model = Semester
		fields = (
					'id',
					'name',
					'university',
					'start',
					'end',
					)

class ProfessorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Professor
		fields = (
					'id',
					'first_name',
					'last_name',
					'title',
					'gender',
					'image',
					'university',
					'email',
					'phone',
					'office',
					'description',
					'rate',
					'ratecount',
					)

class CourseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = (
					'id',
					'fullname',
					'shortname',
					'university',
					'department',
					)

class SectionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Section
		fields = (
					'id',
					'name',
					'semester',
					'course',
					'professor',
					'start',
					'end',
					'description',
					'rate',
					'ratecount',
					)

class LectureSerializer(serializers.ModelSerializer):
	class Meta:
		model = Lecture
		fields = (
					'id',
					'section',
					'weekday',
					'starttime',
					'endtime',
					'location',
					)

