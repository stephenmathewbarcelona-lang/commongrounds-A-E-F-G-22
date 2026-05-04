from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

# Create your models here.

class Profile(models.Model):
    name = models.CharField(max_length=63)

    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE
    )
    
    email = models.TextField(
        blank = True,
        validators = [MinLengthValidator(256)]
    )
    
    def __str__(self):
        return f"{self.name}"