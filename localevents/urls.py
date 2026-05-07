from django.urls import path
from . import views

app_name = 'localevents'

urlpatterns = [
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('event/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('event/add/', views.EventCreateView.as_view(), name='event_create'),
    path('event/<int:pk>/edit/', views.EventUpdateView.as_view(), name='event_update'),
    path('event/<int:pk>/signup/', views.EventSignupView.as_view(), name='event_signup'),
]
