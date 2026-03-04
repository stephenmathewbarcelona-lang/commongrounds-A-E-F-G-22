from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Book, Genre

# Create your views here.
class BookclubBooksView(ListView):
    model = Genre
    template_name = "bookclub_list.html"

class BookclubBooksDetailView(DetailView):
    model = Genre
    template_name = "bookclub_detail.html"