from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm

from .models import Profile, skills
from django.contrib.auth.models import User

from .utils import searchProfiles, paginateProfiles

# Create your views here.

def loginUser(request):

    page = 'Login'


    if request.user.is_authenticated:
        return redirect('all_movies')

    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']


        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User name does not exist')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'Username or password is incorrect')



    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.info(request, 'User logged out')

    return redirect('login')




def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User Account Created')

            login(request, user)

            return redirect('edit-account')
        
        else:
            messages.error(request, 'An Error has Occured with registering user')


    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)




def profiles(request):
    profiles, search_query =  searchProfiles(request)

    paginator, profiles = paginateProfiles(request, profiles, 3)
 
    context = {'profiles': profiles, 'search_query':search_query, 'paginator':paginator}
    return render(request, 'users/profiles.html', context)

def userProfiles(request, pk):
    
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skills_set.exclude(description__exact="")
    otherSkills = profile.skills_set.filter(description="")

    context = {'profile':profile, 'topSkills':topSkills, 'otherSkills':otherSkills}
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skills_set.all()
    movies = profile.movies_set.all()

    context = {'profile':profile, 'skills':skills, 'movies':movies}
    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    
    if request.method=='POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile) #instance = profile -  means that when the form is saved, it will update this existing profile object instead of creating a new one.
        if form.is_valid():
            form.save()
            return redirect('account')
    context= {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'skill Added')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skills_set.get(id=pk)
    form = SkillForm(instance = skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid(): 
            form.save()
            messages.success(request, 'skill updated')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)

def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skills_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        messages.success(request, 'deleted successfully')
        return redirect('account')
    context={'object':skill}
    return render(request, 'delete_template.html', context)

