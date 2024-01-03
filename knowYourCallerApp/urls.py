from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser),
    path('signup/', views.signUpUser),
    path('markSpam/<str:query>/', views.mark_as_spam),
    path('search/name/<str:query>/', views.search_person_by_name, name="search_person_by_name"),
    path('search/number/<str:query>/', views.search_person_by_number, name="search_person_by_number"),
]