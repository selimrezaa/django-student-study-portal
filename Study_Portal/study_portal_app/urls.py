from django.contrib import admin
from django.urls import path
from .views import *


# app_name="study_portal_app"


urlpatterns = [
        path('', index, name='index'),

        path('signup/',signup,name="signup"),
        path('login/',login_request,name='login'),
        path('logout/',user_logout,name='logout'),
        path('profile/', profile,name='profile'),

        path('delete-note/<pk>/', delete_note, name='delete_note'),
        path('homework/', homework, name="homework"),
        path('homework_update/<pk>/', homework_update, name='homework_update'),
        path('youtube/', youtube, name='youtube'),
        path('todo/', todo, name='todo'),
        path('todo_update/<pk>/', todo_update, name='todo_update'),
        path('book/', book, name='book'),
]
