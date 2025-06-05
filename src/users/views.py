from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm

def login_page(request):
    next_url = request.GET.get('next') or request.POST.get('next') or '/'

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect(next_url)
        else:
            return redirect('users:login')
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form, 'next': next_url})

def register_page(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})
