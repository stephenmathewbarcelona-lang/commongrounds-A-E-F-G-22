from django.urls import path
from .views import BooksListView, BooksDetailView

urlpatterns = [
    path('books', BooksListView.as_view(), name="books_list"),
    path('book/<int:pk>', BooksDetailView.as_view(), name='books_detail'),
]

app_name = 'bookclub'