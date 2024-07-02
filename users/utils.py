from .models import Profile, skills

from django.db.models import Q

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



def paginateProfiles(request, profiles, results):

    page = request.GET.get('page')
    results = 3
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)


    return paginator, profiles





def searchProfiles(request):

    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    skillS = skills.objects.filter(name__iexact=search_query)


    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(skills__in=skillS)
        )

    return profiles, search_query
