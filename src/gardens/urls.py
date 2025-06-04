from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [

    path('meditate/<slug:slug>/', views.meditate, name='meditation-room'),
    #path('meditate/', views.meditate, name='meditate'),
]
