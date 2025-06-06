from django.contrib import admin
from .models import Project, ProjectImage

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'category', 'subcategory', 'created_at')
    list_filter = ('category', 'subcategory')
    search_fields = ('title', 'client', 'industry')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]
