from django.test import TestCase
from unittest.mock import Mock, patch
from requests import Response

from .ghibli import GhibliService
from .exceptions import ServiceRequestError, EmptyDataResponseError, JSONResponseError, UnreachableServiceError
from ghibliservice.settings import env


# Create your tests here.
class GetDataTestCase(TestCase):
	"""Tests the get_data method in GhibliService class."""
	def setUp(self):
		self.mock_get_patcher = patch('services.ghibli.requests.get')
		self.mock_get = self.mock_get_patcher.start()

	def tearDown(self):
		self.mock_get_patcher.stop()

	def test_get_data_from_ghibli(self):
		"""Ensures retrieving data from the API service"""
		self.mock_get.return_value.ok = True
		data = [{
			"id": "2baf70d1-42bb-4437-b551-e5fed5a87abe", "title": "Castle in the Sky",
			"original_title": "天空の城ラピュタ", "original_title_romanised": "Tenkū no shiro Rapyuta",
			"description": "The orphan Sheeta inherited a mysterious crystal that links her to the mythical sky.",
			"director": "Hayao Miyazaki", "producer": "Isao Takahata", "release_date": "1986", "running_time": "124",
			"rt_score": "95", "people": ["https://ghibliapi.herokuapp.com/people/"],
			"url": "https://ghibliapi.herokuapp.com/films/2baf70d1-42bb-4437-b551-e5fed5a87abe"
		}]
		self.mock_get.return_value = Mock()
		self.mock_get.return_value.json.return_value = data

		service = GhibliService()
		response_data = service.get_data('films', env('FILMS_FIELDS'))

		self.assertListEqual(response_data, data)

	def test_get_data_from_ghibli_when_response_not_ok(self):
		"""Test returning non 200 HTTP response status from the API service"""
		self.mock_get.return_value.ok = False
		service = GhibliService()
		self.assertRaises(ServiceRequestError, service.get_data, 'films', env('FILMS_FIELDS'))

	def test_get_data_from_ghibli_when_connection_error(self):
		"""Test returning a connection error from the API service"""
		self.mock_get.side_effect = UnreachableServiceError()
		service = GhibliService()
		self.assertRaises(UnreachableServiceError, service.get_data, 'films', env('FILMS_FIELDS'))

	def test_get_data_from_ghibli_when_json_decode_error(self):
		"""Test returning a JSON data decode error caused by empty or non JSON data from the API service"""
		mocked_res = Response()
		mocked_res.status_code = 200
		self.mock_get.return_value = mocked_res

		service = GhibliService()
		self.assertRaises(JSONResponseError, service.get_data, 'films', env('FILMS_FIELDS'))

	def test_get_data_from_ghibli_when_empty_response_error(self):
		"""Test returning an empty JSON object or list of objects from the API service"""
		empty_data = [{}]
		with patch('services.ghibli.requests.get', side_effect=empty_data):
			service = GhibliService()
		self.assertRaises(EmptyDataResponseError, service.get_data, 'films', env('FILMS_FIELDS'))


class GetFilmsTestCase(TestCase):
	"""Tests the get_films method in GhibliService class."""
	def test_get_films_from_get_data(self):
		"""Ensures retrieving response data from the get_data method"""
		films = [{
			"id": "2baf70d1-42bb-4437-b551-e5fed5a87abe", "title": "Castle in the Sky",
			"original_title": "天空の城ラピュタ", "original_title_romanised": "Tenkū no shiro Rapyuta",
			"description": "The orphan Sheeta inherited a mysterious crystal that links her to the mythical sky.",
			"director": "Hayao Miyazaki", "producer": "Isao Takahata", "release_date": "1986", "running_time": "124",
			"rt_score": "95", "url": "https://ghibliapi.herokuapp.com/films/2baf70d1-42bb-4437-b551-e5fed5a87abe"
		}]
		people = [{
			"id": "ba924631-068e-4436-b6de-f3283fa848f0", "name": "Ashitaka", "gender": "male",
			"age": "late teens", "eye_color": "brown", "hair_color": "brown",
			"films": [
				"https://ghibliapi.herokuapp.com/films/2baf70d1-42bb-4437-b551-e5fed5a87abe"
			],
			"url": "https://ghibliapi.herokuapp.com/people/ba924631-068e-4436-b6de-f3283fa848f0"
		}]
		films_people_combined = [{
			"id": "2baf70d1-42bb-4437-b551-e5fed5a87abe", "title": "Castle in the Sky",
			"original_title": "天空の城ラピュタ", "original_title_romanised": "Tenkū no shiro Rapyuta",
			"description": "The orphan Sheeta inherited a mysterious crystal that links her to the mythical sky.",
			"director": "Hayao Miyazaki", "producer": "Isao Takahata", "release_date": "1986", "running_time": "124",
			"rt_score": "95", "people": [{
				"id": "ba924631-068e-4436-b6de-f3283fa848f0", "name": "Ashitaka", "gender": "male",
				"age": "late teens", "eye_color": "brown", "hair_color": "brown",
				"url": "https://ghibliapi.herokuapp.com/people/ba924631-068e-4436-b6de-f3283fa848f0"
			}],
			"url": "https://ghibliapi.herokuapp.com/films/2baf70d1-42bb-4437-b551-e5fed5a87abe"
		}]

		with patch('services.ghibli.GhibliService.get_data', side_effect=[films, people]):
			service = GhibliService()
			response_data = service.get_films()

		self.assertListEqual(response_data['data'], films_people_combined)

	def test_get_films_from_get_data_when_connection_error(self):
		"""Test handling of connection error returned from the get_data method"""
		error_dict = {"data": None, "error": "Connection error: Unable to reach Ghibli's API."}
		with patch('services.ghibli.GhibliService.get_data', side_effect=UnreachableServiceError()):
			service = GhibliService()
			returned_dict = service.get_films()
		self.assertDictEqual(returned_dict, error_dict)

	def test_get_films_from_get_data_when_json_decode_error(self):
		"""Test handling of JSON decode error returned from the get_data method"""
		error_dict = {"data": None, "error": "Error decoding JSON from Ghibli's API."}
		with patch('services.ghibli.GhibliService.get_data', side_effect=JSONResponseError()):
			service = GhibliService()
			returned_dict = service.get_films()
		self.assertDictEqual(returned_dict, error_dict)

	def test_get_films_from_get_data_when_response_not_ok(self):
		"""Test handling of service request error returned from the get_data method"""
		error_dict = {"data": None, "error": "Ghibli's API didn't respond with a valid response."}
		with patch('services.ghibli.GhibliService.get_data', side_effect=ServiceRequestError()):
			service = GhibliService()
			returned_dict = service.get_films()
		self.assertDictEqual(returned_dict, error_dict)

	def test_get_films_from_get_data_when_empty_response_error(self):
		"""Test handling of empty data error returned from the get_data method"""
		error_dict = {"data": None, "error": "Ghibli's API returned an empty list."}

		with patch('services.ghibli.GhibliService.get_data', side_effect=EmptyDataResponseError()):
			service = GhibliService()
			returned_dict = service.get_films()
		self.assertDictEqual(returned_dict, error_dict)
