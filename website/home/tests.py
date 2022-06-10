from django.test import TestCase
from .models import HomePage

class HomePageTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.page = HomePage.objects.get()

    def test_accessible(self):
       response = self.client.get(self.page.url)
       self.assertEqual(response.status_code, 200)
