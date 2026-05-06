from django.db import models
from django.urls import reverse
from django.utils import dates
from useraccounts.models import Profile

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}"
    def get_absolute_url(self):
        return reverse('bookclub:genres', args = [str(self.id)])
    
    class Meta:
        ordering = ['name']
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

class Book(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(
        Genre,
        on_delete = models.SET_NULL,
        null=True,
        related_name = 'book'
    )
    contributor = models.ForeignKey(
        Profile, 
        on_delete = models.SET_NULL, 
        related_name = 'book'
    )
    author = models.CharField()
    synopsis = models.TextField(blank=True)
    publication_year = models.PositiveIntegerField()
    available_to_borrow = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
    
    def get_absolute_url(self):
        return reverse('bookclub:book_detail', kwargs={"pk":self.pk})
    
    class Meta:
        ordering = ['publication_year']
        verbose_name = 'book'
        verbose_name_plural = 'books'

class BookReview(models.Model):
    userReviewer = models.ForeignKey(
        Profile, 
        on_delete = models.CASCADE,
        null = True,
        related_name = 'bookreview'
    )
    anonReviewer = models.TextField(blank=True)
    book = models.ForeignKey(
        Book, 
        on_delete = models.CASCADE,
        null = True,
        related_name = 'bookreview'
    )
    title = models.CharField()
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title}"

class Bookmark(models.Model):
    profile = models.ForeignKey(
        Profile, 
        on_delete = models.CASCADE,
        null = True,
        related_name = 'bookmark'
    )
    book = models.ForeignKey(
        Book, 
        on_delete = models.CASCADE,
        null = True,
        related_name = 'bookmark'
    )
    date_bookmarked = models.DateField()

class Borrow(models.Model):
    book = models.ForeignKey(
        Book, 
        on_delete = models.CASCADE,
        null = True,
        related_name = 'borrow'
    )
    borrower = models.ForeignKey(
        Profile, 
        on_delete = models.CASCADE, 
        related_name = 'borrow'
    )
    name = models.CharField()
    date_borrowed = models.DateField()
    date_returned = models.DateField()