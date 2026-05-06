from django.urls import path
from .views import ProductsListView, ProductDetailView, ProductCreateView, ProductUpdateView, CartView, TransactionslistView

urlpatterns = [
    path('items/', ProductsListView.as_view(), name='productsList'),
    path('item/<int:pk>/', ProductDetailView.as_view(), name='productDetail'),
    path('item/add/', ProductCreateView.as_view(), name='productCreate'),
    path('item/<int:pk>/edit', ProductUpdateView.as_view(), name='productUpdate'),
    path('cart/', CartView.as_view(), name='cart'),
    path('transactions/', TransactionslistView.as_view(), name='transactionsList'),
]

app_name = 'merchstore'