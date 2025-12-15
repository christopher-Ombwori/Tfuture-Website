from django.contrib import admin
from django.utils.html import format_html
from .models import BrandDiscoverySubmission

@admin.register(BrandDiscoverySubmission)
class BrandDiscoverySubmissionAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'rep_name', 'email', 'phone', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('business_name', 'rep_name', 'email', 'phone')
    readonly_fields = ('rep_name', 'business_name', 'email', 'phone', 'additional_responses_display', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('rep_name', 'business_name', 'email', 'phone')
        }),
        ('Additional Information', {
            'fields': ('additional_responses_display',),
            'description': 'Responses from dynamic form sections'
        }),
        ('Management', {
            'fields': ('status', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def additional_responses_display(self, obj):
        """Display additional responses in a readable format"""
        if not obj.additional_responses:
            return "No additional responses"
        
        html = '<div style="padding: 15px; border-radius: 8px;">'
        
        for key, value in obj.additional_responses.items():
            # Format the key (e.g., "question_1_1" -> "Question 1.1")
            formatted_key = key.replace('_', ' ').title()
            
            # Format the value
            if isinstance(value, list):
                formatted_value = ', '.join(str(v) for v in value)
            else:
                # If it's a long text, add line breaks for readability
                formatted_value = str(value).replace('\n', '<br>')
            
            html += f'''
            <div style="margin-bottom: 15px; padding-bottom: 15px; border-bottom: 1px solid #e5e7eb;">
                <strong style="color: #ffffff;">{formatted_key}</strong>
                <div style="color: #ffffff; margin-top: 5px; line-height: 1.5;">{formatted_value}</div>
            </div>
            '''
        
        html += '</div>'
        return format_html(html)
    
    additional_responses_display.short_description = 'Form Responses'
