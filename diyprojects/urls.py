from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.ProjectList_View.as_view(), name='project_list'),
    path('project/<int:pk>/', views.ProjectDetail_View.as_view(), name='project_detail'),
]