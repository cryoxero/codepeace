from django.shortcuts import render, get_object_or_404
from .models import Garden

def meditate(request, slug):
    garden = get_object_or_404(Garden, slug=slug)
    return render(request, 'gardens/meditate.html', {'garden': garden})
