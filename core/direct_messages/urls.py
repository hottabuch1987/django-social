from django.urls import path
from django.shortcuts import render
from . import views

app_name = 'direct_messages'

urlpatterns = [
    path('', views.index, name='my_direct_messages'),
    path('chat/<str:username>/', views.chatPage, name='chat'),
]

