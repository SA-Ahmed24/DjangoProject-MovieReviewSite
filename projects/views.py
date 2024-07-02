from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Movies, Tags
from .forms import MoviesForm, ReviewForm

from django.contrib.auth.decorators import login_required

from django.core.exceptions import ValidationError

from .utils import searchMovie, paginateProject

from django.contrib import messages


def All_Movies(request):

    movies, search_query = searchMovie(request)
    paginator, movies = paginateProject(request, movies, 5)

   
    context = {'movies': movies, 'search_query':search_query, 'paginator':paginator}
    return render(request, 'projects/movies.html', context)

def Selected_Movie(request, pk):
    movieObj = Movies.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.movie = movieObj
        review.owner = request.user.profile
        review.save()

        movieObj.getVoteCount()

        messages.success(request, 'Review Added')

    return render(request, 'projects/selected-movies.html', {'movie':movieObj, 'form':form})

@login_required(login_url='login')
def CreateMovie(request):

    profile = request.user.profile
    form = MoviesForm()

    if request.method == "POST":
        form = MoviesForm(request.POST, request.FILES)
        
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            form.save_m2m()
            return redirect('all_movies')


    context = {f'form': form}
    return render(request, 'projects/project_form.html', context)



@login_required(login_url='login')
def UpdateMovie(request, pk):
    profile = request.user.profile
    movie = profile.movies_set.get(id=pk)
    form = MoviesForm(instance=movie)

    if request.method == "POST":
        form = MoviesForm(request.POST, request.FILES, instance=movie)

        if form.is_valid():
            form.save()
            return redirect('all_movies')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)



@login_required(login_url='login')
def DeleteMovie(request, pk):
    profile = request.user.profile
    movie = profile.movies_set.get(id=pk)

    if request.method == "POST":
        movie.delete()
        return redirect('all_movies')


    context = {'object': movie}
    return render(request, 'delete_template.html', context)

