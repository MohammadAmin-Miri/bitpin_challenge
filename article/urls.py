from django.urls import path

from .views import ArticleAPIView, ReviewAPIView


urlpatterns = [
    path("", ArticleAPIView.as_view(), name="list-article"),
    path("<int:pk>/review/", ReviewAPIView.as_view(), name="review-article"),
]
