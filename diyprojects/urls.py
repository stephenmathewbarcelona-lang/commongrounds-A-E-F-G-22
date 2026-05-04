from django.urls import path
from .views import ProjectList_View, ProjectDetail_View

urlpatterns = [
    path('projects/', ProjectList_View.as_view(), name='project_list'),
    path('project/<int:pk>/', ProjectDetail_View.as_view(), name='project_detail'),
]