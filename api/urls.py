
from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)




urlpatterns = [

    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), #,as_view is being used as we are using a class based view. URL needs a callable (like a function) to handle request. as_view conversts class based view to function based view.
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.getRoutes),
    path('movies/', views.getMovies),
    path('movies/<str:pk>/', views.getMovie),
    path('movies/<str:pk>/vote/', views.movieVote),

]

