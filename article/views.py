from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Article
from .serializers import ArticleSerializer, ReviewSerializer


class ArticleAPIView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]


class ReviewAPIView(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        article = self.get_object()
        serializer.save(article=article, user=self.request.user)
