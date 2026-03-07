from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Project

# Create your views here.
class ProjectList_View(ListView):
    model = Project
    template_name = 'diyprojects/project_list.html'
    context_object_name = "projects"
    


class ProjectDetail_View(DetailView):
    model = Project
    template_name = 'diyprojects/project_detail.html'
    