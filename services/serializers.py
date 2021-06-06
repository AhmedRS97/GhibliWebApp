from rest_framework import serializers


class PeopleSerializer(serializers.Serializer):
	id = serializers.CharField()
	name = serializers.CharField()
	gender = serializers.CharField()
	age = serializers.CharField(allow_blank=True)
	eye_color = serializers.CharField()
	hair_color = serializers.CharField()
	url = serializers.URLField()


class MoviesSerializer(serializers.Serializer):
	id = serializers.CharField()
	title = serializers.CharField()
	original_title = serializers.CharField()
	original_title_romanised = serializers.CharField()
	description = serializers.CharField()
	director = serializers.CharField()
	producer = serializers.CharField()
	release_date = serializers.CharField()
	running_time = serializers.CharField()
	rt_score = serializers.CharField()
	url = serializers.URLField()


class MoviesPeopleSerializer(MoviesSerializer):
	people = serializers.ListField(
		child=PeopleSerializer(required=False)
	)
