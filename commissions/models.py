from django.db import models

# Create your models here.
class CommissionType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        

class Commission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    people_required = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['created_on']