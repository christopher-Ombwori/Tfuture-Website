from django.shortcuts import render, get_object_or_404
from .models import Project

# Create your views here.

def home(request):
    return render(request, 'core/home.html')

def terms(request):
    return render(request, 'core/terms.html')

def about(request):
    return render(request, 'core/about.html')

def portfolio(request): 
    projects = Project.objects.all().order_by('-created_at')
    print("Projects in view:", list(projects.values('title', 'slug')))  # Debug output
    return render(request, 'core/portfolio.html', {
        'projects': projects
    })

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'core/project_detail.html', {
        'project': project
    })