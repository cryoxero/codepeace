from django.shortcuts import render

def home_page(req):
    return render(req, 'index.html')
