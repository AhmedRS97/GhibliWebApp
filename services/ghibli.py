import requests
from json.decoder import JSONDecodeError

from .exceptions import ServiceRequestError, EmptyDataResponseError, JSONResponseError, UnreachableServiceError
from ghibliservice.settings import env


class GhibliService(object):
	"""A class to encapsulate The Ghibli API web service."""
	def __init__(self):
		# get the host of the Ghibli service
		self.host = env('GHIBLI_HOST')
		self.host = self.host.strip('/\\ ')

	def get_data(self, endpoint: str, query_fields: list[str]):
		"""Sends an http request to an external HTTP API service and returns JSON decoded response."""
		try:
			response = requests.get(f'{self.host}/{endpoint}', params={'fields': query_fields})
		except requests.ConnectionError:
			raise UnreachableServiceError
		if not response.ok:
			raise ServiceRequestError()
		# Decode JSON to python data structures, raise error when response data is empty or not JSON.
		try:
			data = response.json()
		except JSONDecodeError:
			raise JSONResponseError()
		if not any(data):
			raise EmptyDataResponseError()
		return data

	def get_films(self):
		"""Runs get_data method to get movies and people data from the API service.

		At the moment, Ghibli's API service have a 'bug' in the films endpoint
		that doesn't list the people related to the film. Thus having the need to
		get all people's data and then append each person to the film they relate to.
		"""
		try:
			movies_data = self.get_data(endpoint='films', query_fields=env('FILMS_FIELDS'))
			people_data = self.get_data(endpoint='people', query_fields=env('PEOPLE_FIELDS'))
		except UnreachableServiceError:
			return {"data": None, "error": "Connection error: Unable to reach Ghibli's API."}
		except JSONResponseError:
			return {"data": None, "error": "Error decoding JSON from Ghibli's API."}
		except ServiceRequestError:
			return {"data": None, "error": "Ghibli's API didn't respond with a valid response."}
		except EmptyDataResponseError:
			return {"data": None, "error": "Ghibli's API returned an empty list."}

		for movie in movies_data:
			people = [person for person in people_data if 'films' in person and movie['url'] in person['films']]
			[person.pop('films') for person in people if 'films' in person]
			movie['people'] = people

		return {"data": movies_data, "error": None}
