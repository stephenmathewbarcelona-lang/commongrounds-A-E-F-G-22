from django.urls import path
from .views import CommissionRequestsListView, CommissionRequestsDetailView, CommisionRequestCreateView, CommisionRequestUpdateView

urlpatterns = [
    path('requests', CommissionRequestsListView.as_view(), name="commissions-list"),
    path('request/<int:pk>', CommissionRequestsDetailView.as_view(), name='commissions-detail'),
    path('request/add', CommisionRequestCreateView.as_view(), name='commissions-create'),
    path('request/<int:pk>/edit', CommisionRequestUpdateView.as_view(), name='commissions-update'), 
    ]

app_name = 'commissions'