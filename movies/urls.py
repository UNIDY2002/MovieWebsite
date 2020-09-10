from django.urls import path

from . import views

urlpatterns = [
    path('actor/<int:pk>/', views.ActorView.as_view(), name='actor')
]
