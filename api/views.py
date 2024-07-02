from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import MoviesSerializer
from projects.models import Movies, Review


@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET':'/api/movies'},
        {'GET':'/api/movies/id'},
        {'POST':'/api/movies/id/vote'},

        {'POST':'/api/users/token'},
        {'POST':'/api/users/token/refresh'},

    ]
    return Response(routes)


@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def getMovies(request):
    #print('USERS:', request.user)
    movies = Movies.objects.all()
    serializer = MoviesSerializer(movies, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def getMovie(request, pk):
    movie = Movies.objects.get(id=pk)
    serializer = MoviesSerializer(movie, many=False)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movieVote(request, pk):
    movie = Movies.objects.get(id=pk)
    user = request.user.profile
    data = request.data

    review, created =Review.objects.get_or_create(
        owner = user,
        movie = movie,
    )

    review.value = data['value']
    review.save()
    movie.getVoteCount()


    print('DATA:', data)

    serializer = MoviesSerializer(movie, many=False)

    return Response(serializer.data)