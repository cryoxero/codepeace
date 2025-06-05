from django.urls import path
from . import views

app_name = 'gardens'

urlpatterns = [

    path('meditate/<slug:slug>/', views.meditate, name='meditation-room'),
    path('temple/<slug:slug>/', views.temple, name='temple'),
    path('', views.gardens, name='list'),
]
