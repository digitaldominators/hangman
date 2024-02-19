from django.test import TestCase

from .models import Category, Phrase


# Create your tests here.
class CategoryTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """create 2 categories with 5 phrases each"""
        for i in range(2):
            category = Category.objects.create(name=f"category {i}")
            for phrase in range(40):
                Phrase.objects.create(phrase=f"phrase {phrase}", category=category)

    def test_list_categories(self):
        """test that the list of categories is correct"""
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_nonactive_category_not_displayed(self):
        """test that non-active categories are not displayed"""
        category = Category.objects.create(name="non-active category", active=False)
        for phrase in range(40):
            Phrase.objects.create(phrase=f"phrase {phrase}", category=category)
        categories = Category.objects.all()
        self.assertEqual(categories.count(), 3)

        response = self.client.get("/api/categories/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_category_with_less_than_20_phrases_not_displayed(self):
        """test that categories with less than 20 phrases are not displayed"""
        category = Category.objects.create(name="less than 20 phrases")
        for phrase in range(10):
            Phrase.objects.create(phrase=f"phrase {phrase}", category=category)
        categories = Category.objects.all()
        self.assertEqual(categories.count(), 3)

        response = self.client.get("/api/categories/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
