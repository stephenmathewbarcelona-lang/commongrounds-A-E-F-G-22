from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Book, Genre

# Create your views here.
class BooksListView(ListView):
    model = Book
    template_name = "book_list.html"
    context_object_name = "book_list"

class BooksDetailView(DetailView):
    model = Book
    template_name = "book_detail.html"
    context_object_name = "book"