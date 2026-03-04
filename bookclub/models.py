from django.db import models

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']

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

    class Meta:
        ordering = ['created_on']