from django.urls import path
from . import views

urlpatterns = [
    path('', views.All_Movies, name="all_movies"),
    path('movie/<str:pk>/', views.Selected_Movie, name="movie"),
    
    path('create-movie/', views.CreateMovie, name='create-movie'),
    path('update-movie/<str:pk>/', views.UpdateMovie, name='update-movie'),
    path('delete-movie/<str:pk>/', views.DeleteMovie, name='delete-movie'),
]