from django.contrib import admin
from .models import ServiceRequest


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "service",
        "status",
        "created_at",
        "source",
    )
    list_filter = ("service", "status", "created_at", "source")
    search_fields = ("first_name", "last_name", "email", "phone", "message")
    list_editable = ("status",)
    
    fieldsets = (
        (
            "Customer Information",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "phone",
                    "service",
                    "message",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Request Management",
            {
                "fields": ("status", "source", "admin_notes"),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        """
        Make all client information readonly to prevent editing.
        Only allow editing of status and admin notes.
        """
        if obj:  # Existing object
            return (
                "first_name",
                "last_name", 
                "email",
                "phone",
                "service",
                "message",
                "source",
                "created_at",
                "updated_at",
            )
        else:
            # For new requests, all fields are readonly since we don't allow creation
            return (
                "first_name",
                "last_name", 
                "email",
                "phone",
                "service",
                "message",
                "source",
                "status",
                "admin_notes",
                "created_at",
                "updated_at",
            )

    def get_fieldsets(self, request, obj=None):
        """
        Return fieldsets for viewing service requests.
        Since we don't allow creation from admin, we only need to handle existing objects.
        """
        return super().get_fieldsets(request, obj)

    def has_add_permission(self, request):
        # Disable adding new requests through admin - they should only come from website
        return False

    def has_delete_permission(self, request, obj=None):
        # Allow deletion for cleanup purposes
        return True

