from django.contrib.auth.models import User
from django.test import TestCase

from accounts.models import UserProfile


# Create your tests here.
class ScoreBoardTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """create 4 users with userprofiles with different scores and games played"""
        scores = [200, 700, 800, 6_000]
        for i in range(len(scores)):
            user = User.objects.create_user(username=f"user {i}", password="password")
            UserProfile.objects.create(user=user, score=scores[i], games_played=(i + 1) * 10)

    def test_scoreboard_total_scores(self):
        """test that the total scores are displayed in the correct order"""
        response = self.client.get("/api/scoreboard/")
        self.assertEqual(response.status_code, 200)
        total_scores_order = [6_000, 800, 700, 200]
        for i, user in enumerate(response.json()["total_scores"]):
            self.assertEqual(user["total_score"], total_scores_order[i])

    def test_scoreboard_average_scores(self):
        """test that the average scores are displayed in the correct order"""
        response = self.client.get("/api/scoreboard/")
        self.assertEqual(response.status_code, 200)
        average_scores_order = [150, 35, 26, 20]
        for i, user in enumerate(response.json()["average_scores"]):
            self.assertEqual(user["avg_score"], average_scores_order[i])
