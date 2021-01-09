from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.home, name='home'),
    path('tag/<slug:slug>/', views.tag, name='tag'),
    path('quiz/create/', views.create, name='create'),
    path('quiz/<slug:slug>/', views.quiz, name='quiz'),
]