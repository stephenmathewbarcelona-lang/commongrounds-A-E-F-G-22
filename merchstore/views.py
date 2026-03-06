from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import ProductType, Product

class MerchStoreListView(ListView):
    model = ProductType
    template_name = "merchstore_list.html"
    context_object_name = 'productType_list'

class MerchStoreDetailView(DetailView):
    model = Product
    template_name = "merchstore_detail.html"
    context_object_name = 'product'