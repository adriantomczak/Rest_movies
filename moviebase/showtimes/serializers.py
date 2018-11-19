from rest_framework import serializers
from showtimes.models import Cinema, Screening


class CinemaSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Cinema
        fields = ('name', 'city', 'movies')


class ScreeningSerializer(serializers.ModelSerializer):
    movie = serializers.SlugRelatedField('title', read_only=True)

    class Meta:
        model = Screening
        fields = ('movie', 'cinema', 'date')
