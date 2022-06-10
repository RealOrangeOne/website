from django.test import SimpleTestCase
from .utils import get_page_models
from .models import BasePage

class BasePageTestCase(SimpleTestCase):
    def test_unique_body_classes(self):
        body_classes = [page.body_class for page in get_page_models()]
        self.assertEqual(len(body_classes), len(set(body_classes)))

    def test_pages_inherit_base_page(self):
        for page_model in get_page_models():
            self.assertTrue(issubclass(page_model, BasePage), f"{page_model} does not inherit from {BasePage}.")
