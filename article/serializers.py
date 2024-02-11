from rest_framework import serializers
from django.db.models import Avg

from .models import Article, Review


class eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4MDkwMzYyLCJpYXQiOjE3MDc2NTgzNjIsImp0aSI6ImJmZDNmZjM0ODYxMjQ0YmQ4ZjY1MTQ3ODcyYTQ3NGYxIiwidXNlcl9pZCI6MX0.2DpaKg2A4ZMfvGuahlNfsA7RFrX6V73GeHwbKHJqpEY(serializers.ModelSerializer):
    users_reviewed_count = serializers.SerializerMethodField()
    review_average = serializers.SerializerMethodField()
    user_point = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ["title", "text", "users_reviewed_count", "review_average", "user_point"]

    def get_users_reviewed_count(self, obj) -> int:
        return Review.objects.filter(article=obj).count()

    def get_review_average(self, obj) -> float:
        return (
            Review.objects.filter(article=obj)
            .aggregate(review_average=Avg("point"))
            .get("review_average")
        )

    def get_user_point(self, obj) -> int:
        user = self.context.get("request").user
        review = Review.objects.filter(article=obj, user=user)
        if not review.exists():
            return None
        return review.first().point


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "article", "user", "point"]
        read_only_fields = ("article", "user")

    def create(self, validated_data):
        point = validated_data.pop("point")
        review, _ = Review.objects.get_or_create(**validated_data)
        review.point = point
        review.save()
        return review
