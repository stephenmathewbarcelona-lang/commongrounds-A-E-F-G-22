from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import ProductType, Product

# Create your views here.
class MerchStoreListView(ListView):
    model = ProductType
    template_name = "merchstore_list.html"

class MerchStoreDetailView(DetailView):
    model = ProductType
    template_name = "merchstore_detail.html"