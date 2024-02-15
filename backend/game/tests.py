from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from .models import GameMap
from category.models import Category, Phrase


# Create your tests here.
class DefaultSettingsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
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
    Test list one game
    Test guess a letter
    Test update timer
    """

    @classmethod
    def setUpTestData(cls):
        """Create a user and a category with phrases for testing"""
        cls.user1 = User.objects.create_user(username="user1", password="password 1")
        cls.user2 = User.objects.create_user(username="user2", password="password 2")
        cls.cat1 = Category.objects.create(name="cat1")
        cat1phrases = ["phrase 1", "phrase 2", "phrase 3"]
        for phrase in cat1phrases:
            Phrase.objects.create(phrase=phrase, category=cls.cat1)

    def test_game_creation_single_player(self):
        """test that a single player game can be created"""
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
        """test that a single player game can be created with a level set"""
        response = self.client.post("/api/game/", {"multiplayer": False, "level": 3})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["level"], 3)

        game_slug = response.json()["game_slug"]
        self.assertTrue(GameMap.objects.filter(game_slug=game_slug, level=3).exists())

    def test_game_creation_player_set_timer(self):
        """test that a single player game can be created with a timer set"""
        response = self.client.post("/api/game/", {"multiplayer": False, "timer": 30})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["timer"], 30)

        game_slug = response.json()["game_slug"]
        self.assertTrue(GameMap.objects.filter(game_slug=game_slug, timer=30).exists())

    def test_game_creation_multiplayer(self):
        """test that a multiplayer game can be created with a word and category"""
        response = self.client.post(
            "/api/game/",
            {"multiplayer": True, "word": "test word", "category_text": "test cat"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["is_multiplayer"], True)
        game_slug = response.json()["game_slug"]
        self.assertTrue(GameMap.objects.filter(game_slug=game_slug).exists())

    def test_game_creation_multiplayer_word_blank(self):
        """test that a multiplayer game can't be created with a blank word"""
        response = self.client.post(
            "/api/game/", {"multiplayer": True, "word": "", "category_text": "test cat"}
        )

        self.assertEqual(response.status_code, 400)

    def test_game_creation_multiplayer_word_required(self):
        """test that a multiplayer game can't be created without a word"""
        response = self.client.post(
            "/api/game/", {"multiplayer": True, "category_text": "test cat"}
        )

        self.assertEqual(response.status_code, 400)

    def test_game_creation_multiplayer_category_required(self):
        """test that a multiplayer game can't be created without a category"""
        response = self.client.post(
            "/api/game/", {"multiplayer": True, "word": "test word"}
        )

        self.assertEqual(response.status_code, 400)

    def test_game_creation_multiplayer_category_blank(self):
        """test that a multiplayer game can't be created with a blank category"""
        response = self.client.post(
            "/api/game/",
            {"multiplayer": True, "word": "test word", "category_text": ""},
        )

        self.assertEqual(response.status_code, 400)

    def test_cant_join_single_player_game(self):
        """test that a single player game can't be joined"""
        self.client.login(username="user1", password="password 1")
        response = self.client.post("/api/game/", {"multiplayer": False})
        game_slug = response.json()["game_slug"]

        self.client.login(username="user2", password="password 2")
        response = self.client.post(f"/api/game/join_game/", {"game_slug": game_slug})
        self.assertEqual(response.status_code, 401)

    def test_multiplayer_game_can_be_joined(self):
        """test that a multiplayer game can be joined"""
        self.client.login(username="user1", password="password 1")
        response = self.client.post(
            "/api/game/",
            {"multiplayer": True, "word": "test word", "category_text": "test cat"},
        )
        game_slug = response.json()["game_slug"]

        self.client.login(username="user2", password="password 2")
        response = self.client.post(f"/api/game/join_game/", {"game_slug": game_slug})
        self.assertEqual(response.status_code, 201)

    def test_multiplayer_game_cannot_be_joined_by_same_player(self):
        """test that the user who created the game cannot join the game as the second user"""
        self.client.login(username="user1", password="password 1")
        response = self.client.post(
            "/api/game/",
            {"multiplayer": True, "word": "test word", "category_text": "test cat"},
        )
        game_slug = response.json()["game_slug"]

        # do not login as a different user here
        response = self.client.post(f"/api/game/join_game/", {"game_slug": game_slug})
        self.assertEqual(response.status_code, 400)

    def test_must_join_game_before_choosing_word(self):
        """test when playing a multiplayer game, the user must join the game before being able to choose the word"""
        self.client.login(username="user1", password="password 1")
        response = self.client.post(
            "/api/game/",
            {"multiplayer": True, "word": "test word", "category_text": "test cat"},
        )
        game_slug = response.json()["game_slug"]

        self.client.login(username="user2", password="password 2")
        response = self.client.post(
            f"/api/game/{game_slug}/choose_word/", {"word": "test word"}
        )
        self.assertEqual(response.status_code, 404)

    def test_joined_user_can_choose_a_word(self):
        """test that the user who joined the game can choose a word"""
        self.client.login(username="user1", password="password 1")
        response = self.client.post(
            "/api/game/",
            {"multiplayer": True, "word": "test word", "category_text": "test cat"},
        )
        game_slug = response.json()["game_slug"]

        self.client.login(username="user2", password="password 2")
        response = self.client.post(f"/api/game/join_game/", {"game_slug": game_slug})
        self.assertEqual(response.status_code, 201)

        response = self.client.post(
            f"/api/game/{game_slug}/choose_word/", {"word": "test word"}
        )
        self.assertEqual(response.status_code, 201)

    def test_list_all_games_logged_in(self):
        """test that all games can be listed"""
        self.client.login(username="user1", password="password 1")
        response = self.client.get("/api/game/")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, [])

        self.client.post("/api/game/", {"multiplayer": False, "level": 3})
        self.client.post("/api/game/", {"multiplayer": False, "timer": 30})

        response = self.client.get("/api/game/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
    def test_list_all_games_anonymous(self):
        """test that all games can be listed"""
        response = self.client.get("/api/game/")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, [])

        self.client.post("/api/game/", {"multiplayer": False, "level": 3})
        self.client.post("/api/game/", {"multiplayer": False, "timer": 30})

        response = self.client.get("/api/game/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)


    def test_view_game_details(self):
        """test that a game can be viewed,
        game is full, timer is 0, level is 1
        status is your turn
        player is 1
        correct guesses is empty
        incorrect guesses is empty
        game_score is 0
        other_player_game_score is 0
        next_turn_time is null
        """
        self.client.login(username='user1', password='password 1')
        response = self.client.post("/api/game/", {'multiplayer': False})
        game_slug = response.json()['game_slug']

        response = self.client.get(f"/api/game/{game_slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['game_slug'], game_slug)
        self.assertEqual(response.json()['is_multiplayer'], False)
        self.assertEqual(response.json()['timer'], 0)
        self.assertEqual(response.json()['level'], 1)
        self.assertEqual(response.json()['status'], 'your turn')
        self.assertEqual(response.json()['player'], 1)
        self.assertEqual(response.json()['correct_guesses'], [])
        self.assertEqual(response.json()['incorrect_guesses'], [])
        self.assertEqual(response.json()['game_score'], 0)
        self.assertEqual(response.json()['other_player_game_score'], None)
        self.assertIsNone(response.json()['next_turn_time'])

    def test_view_game_details_timer_updates(self):
        """test that if the timer is set on a multiplayer game it updates if the next turn time already happened, and sets the turns to [1, 2]"""
        self.client.login(username='user1', password='password 1')
        response = self.client.post("/api/game/", {'multiplayer': True, 'word': 'test word', 'category_text': 'test cat','timer':10})
        game_slug = response.json()['game_slug']

        self.client.login(username='user2', password='password 2')
        self.client.post(f"/api/game/join_game/", {'game_slug': game_slug})

        self.client.post(f"/api/game/{game_slug}/choose_word/", {'word': 'test word'})

        game_map = GameMap.objects.get(game_slug=game_slug)
        self.assertEqual(game_map.turns, [1, 2])

        response = self.client.put(f"/api/game/{game_slug}/", {'guess': 'a'}, content_type='application/json')
        game_map.refresh_from_db()

        self.assertEqual(response.status_code, 200)

        self.assertEqual(game_map.turns, [1])

        # mocking did not work, so I used just set to a date in the past
        game_map.next_turn_time = timezone.now() - timezone.timedelta(days=3)
        game_map.save()
        game_map.refresh_from_db()
        # test that if the time past the next turn time, the timer updates and the turns reset
        self.client.get(f"/api/game/{game_slug}/")


        game_map.refresh_from_db()
        self.assertEqual(game_map.turns, [1, 2])
