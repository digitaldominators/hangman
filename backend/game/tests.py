from django.test import TestCase


# Create your tests here.
class TestTestCase(TestCase):
    def setUp(self):
        pass

    def test_test(self):
        """Test that django test run in github actions"""
        self.assertEqual('The lion says "roar"', 'The lion says "roar"')
