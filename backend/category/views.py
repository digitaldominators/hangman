from django.db.models import Count, Q
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Category
from .serializers import CategorySerializer


# Create your views here.
class CategoryViewSet(viewsets.GenericViewSet):
    def get_queryset(self):
        queryset = (
            Category.objects.filter(active=True)
            .annotate(phrase_count=Count("phrase"))
            .filter(phrase_count__gte=20)
        )
        return queryset

    def list(self, request, *args, **kwargs):
        serializer = CategorySerializer(self.get_queryset(), many=True)
        return Response(serializer.data)
