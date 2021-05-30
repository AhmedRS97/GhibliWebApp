from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.views.decorators.cache import cache_page
from .serializers import MoviesPeopleSerializer
from .fetch_service import get_movies


@api_view(['GET'])
@cache_page(60)
def list_movies(request):
    movies_list = get_movies()
    serializer = MoviesPeopleSerializer(data=movies_list, many=True)

    if serializer.is_valid():
        return Response(serializer.data)

    return HttpResponse("Movies list is not valid", status=500)
