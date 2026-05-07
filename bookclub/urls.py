from django.urls import path
from .views import BooksListView, BooksDetailView, BookCreateView, BookUpdateView, BookBorrowView

urlpatterns = [
    path('books', BooksListView.as_view(), name='books_list'),
    path('book/<int:pk>', BooksDetailView.as_view(), name='books_detail'),
    path('book/add', BookCreateView.as_view(), name='books_create'),
    path('book/<int:pk>/edit', BookUpdateView.as_view(), name='books_update'),
    path('book/<int:pk>/borrow', BookBorrowView.as_view(), name='books_borrow'),
]

app_name = 'bookclub'