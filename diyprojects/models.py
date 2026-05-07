from django.db import models
from django.urls import reverse
from accounts.models import Profile
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
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-created_on']

    def get_absolute_url(self):
        return reverse("project_detail", args=[str(self.id)])

class Favorite(models.Model):
   STATUS_CHOICES = [
       ("Backlog", "Backlog"),
       ("To-Do", "To-Do"),
       ("Done", "Done"),
   ]

   project = models.ForeignKey(Project, on_delete=models.CASCADE,)  
   date_favorited = models.DateTimeField(auto_now_add=True)
   project_status = models.CharField(max_length=20, choices=STATUS_CHOICES)   
   profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
   

class ProjectReview(models.Model):
    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,)
    comment = models.TextField()
    image = models.ImageField(upload_to='review_images/', blank=True, null=True)


class ProjectRating(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,)
    score = models.IntegerField()