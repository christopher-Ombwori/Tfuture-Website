from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'core/home.html')

def terms(request):
    return render(request, 'core/terms.html')

def about(request):
    return render(request, 'core/about.html')
