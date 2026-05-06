from django.urls import path
from .views import ProfileUpdateView

urlpatterns = [
    path('profile/update', ProfileUpdateView.as_view(), name='profile-update')
]

app_name = 'accounts'