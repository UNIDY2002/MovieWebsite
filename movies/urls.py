from django.urls import path

from . import views

urlpatterns = [
    path('', views.MovieList.as_view(), name='base'),
    path('movies/', views.MovieList.as_view(), name='movies'),
    path('actors/', views.ActorList.as_view(), name='actors'),
    path('actor/<int:pk>/', views.ActorView.as_view(), name='actor'),
    path('movie/<int:pk>/', views.MovieView.as_view(), name='movie'),
    path('search', views.search, name='search')
]
