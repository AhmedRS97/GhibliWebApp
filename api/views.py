from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from django.views.decorators.cache import cache_page

from services.serializers import MoviesPeopleSerializer
from services.ghibli import GhibliService


@api_view(['GET'])
@cache_page(60)
def list_movies(request):
    """Movies list endpoint that returns list of films and people."""
    service = GhibliService()
    data = service.get_films()
    movies_list = data['data']
    serializer = MoviesPeopleSerializer(data=movies_list, many=True)

    if data["error"]:
        raise APIException(data["error"])

    return Response(serializer.initial_data)
