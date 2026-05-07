from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from datetime import date, timedelta
from accounts.mixins import RoleRequiredMixin
from .forms import BookForm, BookReviewForm, BookBorrowForm
from .models import Book, Bookmark, BookReview, Borrow

# Create your views here.
class BooksListView(ListView):
    model = Book
    template_name = "book_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_books'] = Book.objects.all()
        current_user = self.request.user.profile
        
        if self.request.user.is_authenticated:
            context['contributed'] = Book.objects.filter(
                contributor = current_user
            )
            context['bookmarked'] = Book.objects.filter(
                bookmark__profile = current_user
            )
            context['reviewed'] = Book.objects.filter(
                bookreview__userReviewer = current_user
            )
            context['all_books'] = Book.objects.exclude(
                contributor = current_user
            ).exclude(
                bookmark__profile = current_user
            ).exclude(
                bookreview__userReviewer = current_user
            )
        return context

class BooksDetailView(DetailView):
    model = Book
    template_name = "book_detail.html"
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        context['bookmark_count'] = Bookmark.objects.filter(
            book = book
        ).count()

        context['is_bookmarked'] = False
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            context['is_bookmarked'] = Bookmark.objects.filter(
                profile=profile).filter(book=self.get_object()).exists()

        context['is_contributor'] = False
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            if self.get_object().contributor == self.request.user.profile:
                context['is_contributor'] = True

        context['book_reviews'] = BookReview.objects.filter(
            book=self.get_object())

        context['review_form'] = BookReviewForm()

        return context

    def post(self, request, *args, **kwargs):
        current_user = None # check muna if theyre logged in
        if self.request.user.is_authenticated:
            current_user = self.request.user.profile

        if 'bookmark' in request.POST:
            bookmark = Bookmark.objects.filter(
                book = self.get_object(),
                profile = current_user
            )

            if bookmark.exists():
                bookmark.delete()
            else:
                Bookmark.objects.create(
                    book = self.get_object(),
                    profile = current_user,
                    date_bookmarked = date.today()
                )
            return redirect(self.get_success_url())
        elif 'review' in request.POST:
            review_form = BookReviewForm(
                request.POST
            )

            if review_form.is_valid():
                if self.get_object().book_reviews.filter(
                    userReviewer = current_user
                    ).exists():
                    book_review = self.get_object().book_reviews.get(
                        userReviewer = current_user
                    )
                    book_review.delete()

                if self.request.user.is_authenticated:
                    review_form.instance.userReviewer = current_user
                else:
                    review_form.instance.anon_reviewer = 'Anonymous'
                review = review_form.save(commit=False)
                review.book = self.get_object()
                review.save()
                return redirect(self.get_success_url())
            else:
                return self.render_to_response(
                    self.get_context_data(review_form = review_form)
                )

        return self.get(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy(
            'bookclub:books_detail',
            kwargs={'pk': self.object.pk}
        )

class BookCreateView(RoleRequiredMixin, CreateView):
    model = Book
    template_name = "book_create.html"
    form_class = BookForm
    required_role = "Book Contributor"

    def form_valid(self, form):
        form.instance.contributor = self.request.user.profile
        response = super().form_valid(form)
        return response
    
    def get_success_url(self):
        return reverse_lazy(
            'bookclub:books_detail', 
            kwargs = {'pk': self.kwargs['pk']}
        )

class BookBorrowView(CreateView):
    model = Borrow
    template_name = "book_borrow.html"
    form_class = BookBorrowForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = Book.objects.get(pk=self.kwargs['pk'])
        context['user'] = self.request.user.profile
        return context

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.borrower = self.request.user.profile
        
        form.instance.book = Book.objects.get(pk=self.kwargs['pk'])
        form.instance.date_returned = form.instance.date_borrowed + timedelta(weeks=2)
        form.instance.book.available_to_borrow = False
        form.instance.book.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy(
            'bookclub:books_detail',
            kwargs = {'pk': self.kwargs['pk']}
        )