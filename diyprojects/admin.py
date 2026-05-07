from django.contrib import admin
from .models import Favorite, Project, ProjectCategory, ProjectRating, ProjectReview

# Register your models here.


class ProjectAdmin(admin.ModelAdmin):
    model = Project

class ProjectCategoryAdmin(admin.ModelAdmin):
    model = ProjectCategory

class FavoriteAdmin(admin.ModelAdmin):
    model = Favorite

class ProjectReviewAdmin(admin.ModelAdmin):
    model = ProjectReview

class ProjectRatingAdmin(admin.ModelAdmin):
    model = ProjectRating

admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectCategory, ProjectCategoryAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ProjectReview, ProjectReviewAdmin)
admin.site.register(ProjectRating, ProjectRatingAdmin)