from rest_framework.test import APITestCase
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .serializers import MoviesSerializer, PeopleSerializer
from .fetch_service import fetch, get_movies
from .exceptions import UnreachableServiceError, ServiceRequestError, InvalidResponseDataError


# Create your tests here.
class MoviesListAPIViewTestCase(APITestCase):
	def test_get_movies(self):
		"""
		Ensures retrieving a list of movies and its validity.
		"""
		url = reverse('movies')
		response = self.client.get(url)
		response_serialized_movies = MoviesSerializer(data=response.data, many=True)
		self.assertEqual(response_serialized_movies.is_valid(), True)
		self.assertEqual(response.status_code, status.HTTP_200_OK)


class FetchServiceTestCase(TestCase):
	def setUp(self):
		self.movies_fields = [
			'id', 'title', 'original_title',
			'original_title_romanised', 'description', 'director',
			'producer', 'release_date', 'running_time',
			'rt_score', 'url'
		]
		self.people_fields = [
			'id', 'name', 'gender',
			'age', 'eye_color', 'hair_color',
			'films', 'url'
		]

		self.invalid_fields = ['invalid_field1']

	def test_fetch_data_from_ghibli(self):
		"""
		Ensures retrieving movies or people data and its validity
		"""
		movies = fetch('films', self.movies_fields)
		serialized_movies = MoviesSerializer(data=movies, many=True)

		people = fetch('people', self.people_fields)
		serialized_people = PeopleSerializer(data=people, many=True)

		self.assertEqual(serialized_movies.is_valid(), True)
		self.assertEqual(serialized_people.is_valid(), True)

	def test_fetch_data_with_invalid_fields(self):
		"""
		tests for fetch function raises by providing it with invalid fields.
		"""
		self.assertRaises(InvalidResponseDataError, fetch, 'films', self.invalid_fields)
		self.assertRaises(InvalidResponseDataError, fetch, 'people', self.invalid_fields)

	def test_fetch_data_with_invalid_endpoint(self):
		"""
		tests the fetch function for invalid endpoint error by providing it with invalid endpoint.
		"""
		self.assertRaises(ServiceRequestError, fetch, 'Filmyy', self.movies_fields)
		self.assertRaises(ServiceRequestError, fetch, 'Humanss', self.people_fields)

	def test_fetch_data_with_invalid_url(self):
		"""
		tests the fetch function for broken or non Ghibli API URL.
		"""
		self.assertRaises(ServiceRequestError, fetch, 'films', self.movies_fields, "http://herokuappp.com/")
		self.assertRaises(ServiceRequestError, fetch, 'films', self.movies_fields, "http://example.com/")

