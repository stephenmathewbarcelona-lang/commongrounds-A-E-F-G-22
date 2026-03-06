from django.db import models
from django.urls import reverse

# Create your models here.
class ProjectCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']



class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True, related_name='projects')
    materials = models.TextField()
    steps = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)   

    class Meta:
        ordering = ['-created_on']

    def get_absolute_url(self):
        return reverse("project_detail", args=[str(self.id)])
        
   
