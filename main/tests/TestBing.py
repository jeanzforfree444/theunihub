from django.test import TestCase, Client

from django.urls import reverse

from main.bing_search import run_query

import requests_mock

import json, requests, os



class BingSearchTest(TestCase):

    def setUp(self):

        self.client = Client()
        self.mock_response = {
            "webPages": {
                "value": [
                    {
                        "name": "Django Framework",
                        "url": "https://www.djangoproject.com/",
                        "snippet": "Django is a high-level Python web framework"
                    },
                    {
                        "name": "Django Tutorial",
                        "url": "https://docs.djangoproject.com/en/stable/intro/tutorial01/",
                        "snippet": "Django tutorial to help you get started"
                    }
                ]
            }
        }
    
    @requests_mock.Mocker()
    def test_run_query_function(self, mock_request):

        mock_request.get(
            "https://api.bing.microsoft.com/v7.0/search",
            json=self.mock_response,
            status_code=200
        )

        results = run_query("Django")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["title"], "Django Framework")
        self.assertEqual(results[0]["link"], "https://www.djangoproject.com/")

    
    @requests_mock.Mocker()
    def test_bing_search_view(self, mock_request):

        mock_request.get(
            "https://api.bing.microsoft.com/v7.0/search",
            json=self.mock_response,
            status_code=200
        )

        response = self.client.get(reverse("bing_search"), {"q":"Django"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django Framework")
        self.assertContains(response, "https://www.djangoproject.com/")