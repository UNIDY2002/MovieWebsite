from django.urls import path

from . import views

urlpatterns = [
    path('actor/<int:pk>/', views.ActorView.as_view(), name='actor'),
    path('movie/<int:pk>', views.MovieView.as_view(), name='movie'),
]
