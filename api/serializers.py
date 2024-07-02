from rest_framework import serializers
from projects.models import Movies, Tags, Review
from users.models import Profile



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'


class MoviesSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()
    class Meta:
        model = Movies
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializers = ReviewSerializer(reviews, many=True)
        return serializers.data
