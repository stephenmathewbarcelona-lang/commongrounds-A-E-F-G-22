from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Book, Genre

# Create your views here.
class BooksListView(ListView):
    model = Genre
    template_name = "bookclub_list.html"

class BooksDetailView(DetailView):
    model = Genre
    template_name = "bookclub_detail.html"