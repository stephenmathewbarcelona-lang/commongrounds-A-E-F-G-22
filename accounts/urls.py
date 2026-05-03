from django.urls import path
from .views import AA, AA

urlpatterns = [
    path('acounts/AAUSERNAME', AA.as_view(), name='AA'),
]

app_name = 'accounts'