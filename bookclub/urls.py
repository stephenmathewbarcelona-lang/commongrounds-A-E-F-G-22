from django.urls import path
from .views import BookclubBooksView, BookclubBooksDetailView

urlpatterns = [
    path('bookclub/books', BookclubBooksView.as_view(), name="books-list"),
    path('bookclub/book/<int:pk>', BookclubBooksDetailView.as_view(), name='books-detail'),
]

app_name = 'bookclub'