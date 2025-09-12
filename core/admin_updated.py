from django.contrib import admin
from .models import ServiceRequest, Service


class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'service', 'status', 'created_at')
    list_filter = ('status', 'service', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'message')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status',)
    fieldsets = (
        ('Client Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Request Details', {
            'fields': ('service', 'message', 'status', 'source')
        }),
        ('Admin', {
            'fields': ('admin_notes', 'created_at', 'updated_at')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        # Make client info readonly, don't allow creating new requests
        if obj:  # editing an existing object
            return self.readonly_fields + ('first_name', 'last_name', 'email', 'phone', 'message', 'service', 'source')
        return self.readonly_fields

    def get_fieldsets(self, request, obj=None):
        # Use the fieldsets from the parent class
        return super().get_fieldsets(request, obj)

    def has_add_permission(self, request):
        # Disable adding new service requests through admin
        return False

    def has_delete_permission(self, request, obj=None):
        # Allow deleting service requests
        return True


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_visible', 'is_featured', 'order')
    list_filter = ('is_visible', 'is_featured')
    search_fields = ('name', 'description', 'short_description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_visible', 'is_featured', 'order')
    fieldsets = (
        ('Service Information', {
            'fields': ('name', 'slug', 'description', 'short_description', 'icon_svg')
        }),
        ('Display Options', {
            'fields': ('is_visible', 'order', 'is_featured')
        }),
    )


# Register models with Django Admin
admin.site.register(ServiceRequest, ServiceRequestAdmin)
admin.site.register(Service, ServiceAdmin)