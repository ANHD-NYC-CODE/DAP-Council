from django.test import TestCase
from django.urls import include, path
from rest_framework.test import APITestCase, URLPatternsTestCase
from app.tests.base_test import BaseTest

from datasets import views as v
import logging
logging.disable(logging.CRITICAL)


class CouncilViewTests(BaseTest, TestCase):

    def tearDown(self):
        self.clean_tests()

    def test_list(self):
        self.council_factory()
        self.council_factory()

        response = self.client.get('/councils/', format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 2)

    def test_retrieve(self):
        self.council_factory(id=1)

        response = self.client.get('/councils/1/')
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["id"], 1)

    def test_council_properties(self):
        council = self.council_factory(id=1)
        self.property_factory(council=council, bbl="1")
        self.property_factory(council=council, bbl="2")

        response = self.client.get('/councils/1/properties/')
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 2)

    def test_council_summary(self):
        council = self.council_factory(id=1)

        response = self.client.get('/councils/1/summary/')
        content = response.data

        self.assertEqual(response.status_code, 200)
