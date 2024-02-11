from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator


user_model = get_user_model()


class TimestampBaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        proxy = True


class Article(TimestampBaseModel):
    title = models.CharField(max_length=128)
    text = models.TextField()

    def __str__(self) -> str:
        return str(self.title)

    # @property
    # def users_reviewed(self):
    #     return Review.objects.filter(article=self).count()

    # @property
    # def review_average(self):
    #     return (
    #         Review.objects.filter(article=self)
    #         .aggregate(review_average=models.Avg("point"))
    #         .get("review_average")
    #     )


class Review(TimestampBaseModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    point = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5)])

    class Meta:
        indexes = [
            models.Index(fields=["article"]),
            models.Index(
                fields=["user"],
            ),
        ]
        unique_together = [["article", "user"]]
