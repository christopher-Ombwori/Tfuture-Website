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
    )
    list_filter = ("service", "status", "created_at")
    search_fields = ("first_name", "last_name", "email", "phone", "message")
    list_editable = ("status",)
    readonly_fields = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "service",
        "message",
        "created_at",
        "updated_at",
    )

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
                "fields": ("status", "admin_notes"),
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

    def has_add_permission(self, request):
        # Prevent adding new requests through admin
        return False

    def has_delete_permission(self, request, obj=None):
        # Allow deletion for cleanup purposes
        return True
