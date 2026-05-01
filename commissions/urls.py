from django.urls import path
from .views import CommissionRequestsListView, CommissionRequestsDetailView

urlpatterns = [
    path('requests', CommissionRequestsListView.as_view(), name="commissions-list"),
    path('request/<int:pk>', CommissionRequestsDetailView.as_view(), name='commissions-detail'),
]

app_name = 'commissions'