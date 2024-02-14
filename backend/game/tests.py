from django.test import TestCase
from django.contrib.auth.models import User

from .models import GameMap
from category.models import Category, Phrase


# Create your tests here.
class DefaultSettingsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("test")
        print("test")
        cls.user1 = User.objects.create_user(username="user1", password="password 1")

    def test_get_default_settings_for_authenticated_user(self):
        self.client.login(username="user1", password="password 1")
        response = self.client.get("/api/settings/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"level": 1, "timer": 0})

    def test_set_default_settings_for_authenticated_user(self):
        self.client.login(username="user1", password="password 1")

        self.client.post("/api/settings/", {"level": 2})
        self.client.post("/api/settings/", {"timer": 20})

        response = self.client.get("/api/settings/")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"level": 2, "timer": 20})

    def test_default_settings_invalid_for_authenticated_user(self):
        self.client.login(username="user1", password="password 1")
        response = self.client.post("/api/settings/", {"level": 7})
        # assert invalid level
        self.assertEqual(response.status_code, 400)

        response = self.client.post("/api/settings/", {"timer": -5})
        # assert invalid timer
        self.assertEqual(response.status_code, 400)

        # assert settings stay the same
        response = self.client.get("/api/settings/")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"level": 1, "timer": 0})

    def test_get_default_settings_for_anonymous_user(self):
        response = self.client.get("/api/settings/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"level": 1, "timer": 0})

    def test_set_default_settings_for_anonymous_user(self):
        self.client.post("/api/settings/", {"level": 2})
        self.client.post("/api/settings/", {"timer": 20})

        response = self.client.get("/api/settings/")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"level": 2, "timer": 20})

    def test_default_settings_invalid_for_anonymous_user(self):
        response = self.client.post("/api/settings/", {"level": 7})
        # assert invalid level
        self.assertEqual(response.status_code, 400)

        response = self.client.post("/api/settings/", {"timer": -5})
        # assert invalid timer
        self.assertEqual(response.status_code, 400)

        # assert settings stay the same
        response = self.client.get("/api/settings/")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"level": 1, "timer": 0})


class GameTestCase(TestCase):
    """
    Test creating a new game
    Test Join a game
    Test Choose a word
    Test list all games
    Test list one game
    Test guess a letter
    Test update timer
    """

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username="user1", password="password 1")
        cls.cat1 = Category.objects.create(name="cat1")
        cat1phrases = ["phrase 1", "phrase 2", "phrase 3"]
        for phrase in cat1phrases:
            Phrase.objects.create(phrase=phrase, category=cls.cat1)

    def test_game_creation_single_player(self):
        response = self.client.post("/api/game/", {"multiplayer": False})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["is_multiplayer"], False)

        game_slug = response.json()["game_slug"]
        self.assertTrue(GameMap.objects.filter(game_slug=game_slug).exists())
        self.assertTrue(
            GameMap.objects.filter(game_slug=game_slug, level=1, timer=0).exists()
        )
        self.assertIsNotNone(GameMap.objects.get(game_slug=game_slug).game_1)
        self.assertIsNone(GameMap.objects.get(game_slug=game_slug).game_2)

    def test_game_creation_player_set_level(self):
        response = self.client.post("/api/game/", {"multiplayer": False, "level": 3})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["level"], 3)

        game_slug = response.json()["game_slug"]
        self.assertTrue(GameMap.objects.filter(game_slug=game_slug, level=3).exists())

    def test_game_creation_player_set_timer(self):
        response = self.client.post("/api/game/", {"multiplayer": False, "timer": 30})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["timer"], 30)

        game_slug = response.json()["game_slug"]
        self.assertTrue(GameMap.objects.filter(game_slug=game_slug, timer=30).exists())

    def test_game_creation_multiplayer(self):
        response = self.client.post(
            "/api/game/",
            {"multiplayer": True, "word": "test word", "category_text": "test cat"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["is_multiplayer"], True)
        game_slug = response.json()["game_slug"]
        self.assertTrue(GameMap.objects.filter(game_slug=game_slug).exists())

    def test_game_creation_multiplayer_word_blank(self):
        response = self.client.post(
            "/api/game/", {"multiplayer": True, "word": "", "category_text": "test cat"}
        )

        self.assertEqual(response.status_code, 400)

    def test_game_creation_multiplayer_word_required(self):
        response = self.client.post(
            "/api/game/", {"multiplayer": True, "category_text": "test cat"}
        )

        self.assertEqual(response.status_code, 400)

    def test_game_creation_multiplayer_category_required(self):
        response = self.client.post(
            "/api/game/", {"multiplayer": True, "word": "test word"}
        )

        self.assertEqual(response.status_code, 400)

    def test_game_creation_multiplayer_category_blank(self):
        response = self.client.post(
            "/api/game/",
            {"multiplayer": True, "word": "test word", "category_text": ""},
        )

        self.assertEqual(response.status_code, 400)
