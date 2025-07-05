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
    list_display = ('first_name', 'last_name', 'email', 'phone', 'service', 'status', 'created_at')
    list_filter = ('service', 'status', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'message')
    list_editable = ('status',)
    readonly_fields = ('first_name', 'last_name', 'email', 'phone', 'service', 'message', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'service', 'message'),
            'classes': ('collapse',)
        }),
        ('Request Management', {
            'fields': ('status', 'admin_notes'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Prevent adding new requests through admin
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Allow deletion for cleanup purposes
        return True
