from django.db import models
from django.urls import reverse

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
        on_delete = models.CASCADE,
        related_name = 'book'
    )
    author = models.CharField()
    publication_year = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
    def get_absolute_url(self):
        return reverse('bookclub:book_detail', kwargs={"pk":self.pk})
    
    class Meta:
        ordering = ['created_on']
        verbose_name = 'book'
        verbose_name_plural = 'books'