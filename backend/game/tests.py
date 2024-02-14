from django.test import TestCase
from django.contrib.auth.models import User


# Create your tests here.
class DefaultSettingsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='user1', password='password 1')

    def test_get_default_settings_for_authenticated_user(self):
        self.client.login(username='user1', password='password 1')
        response = self.client.get("/api/settings/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'level': 1, 'timer': 0})

    def test_set_default_settings_for_authenticated_user(self):
        self.client.login(username='user1', password='password 1')

        self.client.post("/api/settings/", {'level': 2})
        self.client.post("/api/settings/", {'timer': 20})

        response = self.client.get("/api/settings/")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'level': 2, 'timer': 20})

    def test_default_settings_invalid_for_authenticated_user(self):
        self.client.login(username='user1', password='password 1')
        response = self.client.post("/api/settings/", {'level': 7})
        # assert invalid level
        self.assertEqual(response.status_code, 400)

        response = self.client.post("/api/settings/", {'timer': -5})
        # assert invalid timer
        self.assertEqual(response.status_code, 400)

        # assert settings stay the same
        response = self.client.get("/api/settings/")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'level': 1, 'timer': 0})

    def test_get_default_settings_for_anonymous_user(self):
        response = self.client.get("/api/settings/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'level': 1, 'timer': 0})

    def test_set_default_settings_for_anonymous_user(self):
        self.client.post("/api/settings/", {'level': 2})
        self.client.post("/api/settings/", {'timer': 20})

        response = self.client.get("/api/settings/")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'level': 2, 'timer': 20})

    def test_default_settings_invalid_for_anonymous_user(self):
        response = self.client.post("/api/settings/", {'level': 7})
        # assert invalid level
        self.assertEqual(response.status_code, 400)

        response = self.client.post("/api/settings/", {'timer': -5})
        # assert invalid timer
        self.assertEqual(response.status_code, 400)

        # assert settings stay the same
        response = self.client.get("/api/settings/")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'level': 1, 'timer': 0})
