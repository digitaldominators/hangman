from rest_framework import viewsets
from rest_framework.response import Response

from accounts.models import UserProfile
from .serializers import TotalScoreboardSerializer,AverageScoreboardSerializer


# Create your views here.
class ScoreboardViewSet(viewsets.GenericViewSet):
    def list(self, request, *args, **kwargs):
        total_scores = UserProfile.objects.filter(score__gt=0).order_by('-score')[:50]
        average_scores = UserProfile.objects.filter(avg_score__isnull=False).order_by('-avg_score')[:50]

        total_scores_serializer = TotalScoreboardSerializer(total_scores, many=True)
        average_scores_serializer = AverageScoreboardSerializer(average_scores, many=True)
        return Response({"total_scores": total_scores_serializer.data,
                         "average_scores": average_scores_serializer.data})
