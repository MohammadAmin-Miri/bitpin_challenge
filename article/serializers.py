from rest_framework import serializers
from django.db.models import Avg

from .models import Article, Review


class ArticleSerializer(serializers.ModelSerializer):
    users_count = serializers.SerializerMethodField()
    review_average = serializers.SerializerMethodField()
    user_point = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ["title", "text", "users_count", "review_average", "user_point"]

    def get_users_count(self, obj):
        return Review.objects.filter(article=obj).count()

    def get_review_average(self, obj):
        return (
            Review.objects.filter(article=obj)
            .aggregate(review_average=Avg("point"))
            .get("review_average")
        )

    def get_user_point(self, obj):
        user = self.context.get("request").user
        review = Review.objects.filter(article=obj, user=user)
        if not review.exists():
            return None
        return review.first().point


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["article", "user", "point"]
        read_only_fields = ("article", "user")
