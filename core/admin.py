from django.contrib import admin
from .models import Project, ProjectImage, Service, ServiceRequest

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'is_featured', 'order', 'created_at')
    list_filter = ('is_active', 'is_featured')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'is_featured', 'order')
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'description', 'short_description')
        }),
        ('Display', {
            'fields': ('is_active', 'is_featured', 'order')
        }),
        ('Icon', {
            'fields': ('icon_svg',),
            'description': 'Paste the full SVG code here (including the <svg> tags)'
        }),
    )

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'category', 'subcategory', 'created_at')
    list_filter = ('category', 'subcategory')
    search_fields = ('title', 'client', 'industry')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # Add JavaScript to show/hide subcategory field based on category
        class Media:
            js = ('admin/js/project_admin.js',)
        
        form.Media = Media
        return form

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'service', 'created_at')
    list_filter = ('service', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'message')
    readonly_fields = ('created_at',)
