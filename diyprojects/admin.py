from django.contrib import admin
from .models import Project, ProjectCategory

# Register your models here.


class ProjectAdmin(admin.ModelAdmin):
    model = Project

class ProjectCategoryAdmin(admin.ModelAdmin):
    model = ProjectCategory

admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectCategory, ProjectCategoryAdmin)