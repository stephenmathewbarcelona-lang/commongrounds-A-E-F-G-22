from django.urls import path
from .views import CommissionRequestsListView, CommissionRequestsDetailView

urlpatterns = [
    path('commissions/requests', CommissionRequestsListView.as_view(), name="commissions-list"),
    path('commissions/request/<int:pk>', CommissionRequestsDetailView.as_view(), name='commissions-detail'),
]

app_name = 'commissions'
