import json
import requests
from .exceptions import UnreachableServiceError, ServiceRequestError, InvalidResponseDataError


api_url = 'https://ghibliapi.herokuapp.com/'

movies_fields = [
		'id', 'title', 'original_title',
		'original_title_romanised', 'description', 'director',
		'producer', 'release_date', 'running_time',
		'rt_score', 'url'
]

people_fields = [
		'id', 'name', 'gender',
		'age', 'eye_color', 'hair_color',
		'films', 'url'
]


def fetch(endpoint: str = None, query_fields: list = None, url: str = None):
	if url is None:
		url = api_url
	if endpoint is None:
		raise ValueError('endpoint parameter is required.')
	if query_fields is None:
		raise ValueError('query_fields parameter is required.')
	url = url.strip('/\\ ')
	query = '?fields=' + ','.join(query_fields)
	try:
		response = requests.get(f'{url}/{endpoint}{query}')
	except requests.ConnectionError:
		raise UnreachableServiceError()

	if response.status_code != 200:
		e = ServiceRequestError()
		e.status_code = response.status_code
		raise e

	try:
		data = response.json()
	except json.decoder.JSONDecodeError:
		raise ServiceRequestError()

	if not any(data):
		raise InvalidResponseDataError()

	return data


def get_movies(fields_movies: list = None, fields_people: list = None):

	if fields_movies is None:
		fields_movies = movies_fields
	if fields_people is None:
		fields_people = people_fields

	movies_data = fetch(endpoint='films', query_fields=fields_movies)
	people_data = fetch(endpoint='films', query_fields=fields_people)

	for movie in movies_data:
		people = [person for person in people_data if 'films' in person and movie['url'] in person['films']]
		[person.pop('films') for person in people if 'films' in person]
		movie['people'] = people

	return movies_data
