from .models import Movies, Tags

from django.db.models import Q

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



def paginateProject(request, movies, results):

    page = request.GET.get('page')
    results = 3
    paginator = Paginator(movies, results)

    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        movies = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        movies = paginator.page(page)


    return paginator, movies





def searchMovie(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    tags = Tags.objects.filter(name__icontains=search_query)

    movies = Movies.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    )
    
    return movies, search_query
