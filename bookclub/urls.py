from django.urls import path
from .views import BooksListView, BooksDetailView

urlpatterns = [
    path('bookclub/books', BooksListView.as_view(), name="books-list"),
    path('bookclub/book/<int:pk>', BooksDetailView.as_view(), name='books-detail'),
]

app_name = 'bookclub'