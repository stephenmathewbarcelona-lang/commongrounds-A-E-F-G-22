from django.urls import path
from .views import MerchStoreListView, MerchStoreDetailView

urlpatterns = [
    path('merchstore/items', MerchStoreListView.as_view(), name='merchstore-list'),
    path('merchstore/item/<int:pk>', MerchStoreDetailView.as_view(), name='merchstore-detail'),
]

app_name = 'merchstore'