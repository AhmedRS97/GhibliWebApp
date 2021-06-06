from rest_framework.test import APITestCase
from rest_framework.exceptions import APIException
from unittest.mock import Mock, patch
from django.urls import reverse
from rest_framework import status

from services.serializers import MoviesSerializer


# Create your tests here.
class MoviesAPIViewTestCase(APITestCase):
	"""Tests the list_movies API view."""

	def test_get_movies(self):
		"""Ensures retrieving a list of movies and people related."""
		data = [{
			"id": "2baf70d1-42bb-4437-b551-e5fed5a87abe", "title": "Castle in the Sky",
			"original_title": "天空の城ラピュタ", "original_title_romanised": "Tenkū no shiro Rapyuta",
			"description": "The orphan Sheeta inherited a mysterious crystal that links her to the mythical sky.",
			"director": "Hayao Miyazaki", "producer": "Isao Takahata", "release_date": "1986", "running_time": "124",
			"rt_score": "95", "people": ["https://ghibliapi.herokuapp.com/people/"],
			"url": "https://ghibliapi.herokuapp.com/films/2baf70d1-42bb-4437-b551-e5fed5a87abe"
		}]
		with patch('services.ghibli.GhibliService.get_films', return_value={"data": data, "error": None}):
			url = reverse('movies')
			response = self.client.get(url)
			response_serialized_movies = MoviesSerializer(data=response.data, many=True)

		self.assertEqual(response_serialized_movies.is_valid(), True)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
