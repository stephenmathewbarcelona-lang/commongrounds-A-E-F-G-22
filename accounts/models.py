from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

# Create your models here.

class Profile(models.Model):
    name = models.CharField(max_length=63)

    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE,
    )
    
    email = models.EmailField(unique=True,
                              null=True, 
                              blank=True)
    
    role = models.CharField(
        max_length=255, 
        choices=[
            ("Market Seller", "Market Seller"),
            ("Event Organizer", "Event Organizer"),
            ("Book Contributor", "Book Contributor"),
            ("Project Creator", "Project Creator"),
            ("Commission Maker", "Commission Maker"),
        ],
        null=True,
        blank=True,
    )
    
    def __str__(self):
        return f"{self.name}"