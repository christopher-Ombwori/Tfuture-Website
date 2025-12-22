from django.contrib import admin
from django import forms
from django.utils import timezone
from django.utils.html import format_html, format_html_join

from .models import PrivacyPolicyPage, TermsOfServicePage


class PrivacyPolicyPageAdminForm(forms.ModelForm):
    add_comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 2}),
        label="Add change note",
        help_text="Append-only note; does not change content.",
    )

    class Meta:
        model = PrivacyPolicyPage
        fields = []  # prevent editing content fields in Django admin


@admin.register(PrivacyPolicyPage)
class PrivacyPolicyPageAdmin(admin.ModelAdmin):
    """Expose Privacy Policy update logs in Django admin (read-only, append-only comments)."""

    form = PrivacyPolicyPageAdminForm
    list_display = ["title", "updates_count", "last_update"]
    readonly_fields = ["title", "updates_log_display"]
    fields = ["title", "updates_log_display", "add_comment"]

    def updates_count(self, obj):
        return len(obj.updates_log or [])

    updates_count.short_description = "Updates"

    def last_update(self, obj):
        if obj.updates_log:
            last = obj.updates_log[-1].value
            return f"{last.get('at')} by {last.get('by') or '—'}"
        return "—"

    last_update.short_description = "Last update"

    def updates_log_display(self, obj):
        if not obj.updates_log:
            return "No updates yet"
        rows = []
        for block in reversed(obj.updates_log):  # newest first
            val = block.value
            ts = val.get("at")
            # Format timestamp as YYYY-MM-DD HH:MM (localtime)
            if ts:
                try:
                    ts = timezone.localtime(ts).strftime("%Y-%m-%d %H:%M")
                except Exception:
                    ts = str(ts)
            rows.append((ts or "—", val.get("by") or "—", val.get("note") or ""))
        return format_html(
            "<table style='border-collapse:collapse;width:100%;font-family:monospace;'>"
            "<thead><tr>"
            "<th style='text-align:left;padding:4px;border-bottom:1px solid #ccc;'>When</th>"
            "<th style='text-align:left;padding:4px;border-bottom:1px solid #ccc;'>Who</th>"
            "<th style='text-align:left;padding:4px;border-bottom:1px solid #ccc;'>Note</th>"
            "</tr></thead><tbody>{}</tbody></table>",
            format_html_join(
                "",
                "<tr>"
                "<td style='padding:4px;border-bottom:1px solid #eee;'>{0}</td>"
                "<td style='padding:4px;border-bottom:1px solid #eee;'>{1}</td>"
                "<td style='padding:4px;border-bottom:1px solid #eee;'>{2}</td>"
                "</tr>",
                rows,
            ),
        )

    updates_log_display.short_description = "Change Log"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        """Append a comment-only log entry; keep all fields read-only for integrity."""
        comment = form.cleaned_data.get("add_comment") if hasattr(form, "cleaned_data") else None
        if comment:
            entry = {
                "at": timezone.now(),
                "by": getattr(getattr(request, "user", None), "username", ""),
                "note": f"Comment: {comment}",
            }
            new_value = list(obj.updates_log) if obj.updates_log else []
            new_value.append({"type": "update", "value": entry})
            obj.updates_log = new_value
            obj.save(update_fields=["updates_log"])
        # Do not call super() to avoid altering other fields; admin acts append-only.


class TermsOfServicePageAdminForm(forms.ModelForm):
    add_comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 2}),
        label="Add change note",
        help_text="Append-only note; does not change content.",
    )

    class Meta:
        model = TermsOfServicePage
        fields = []


@admin.register(TermsOfServicePage)
class TermsOfServicePageAdmin(admin.ModelAdmin):
    """Expose Terms of Service update logs in Django admin (read-only, append-only comments)."""

    form = TermsOfServicePageAdminForm
    list_display = ["title", "updates_count", "last_update"]
    readonly_fields = ["title", "updates_log_display"]
    fields = ["title", "updates_log_display", "add_comment"]

    def updates_count(self, obj):
        return len(obj.updates_log or [])

    updates_count.short_description = "Updates"

    def last_update(self, obj):
        if obj.updates_log:
            last = obj.updates_log[-1].value
            return f"{last.get('at')} by {last.get('by') or '—'}"
        return "—"

    last_update.short_description = "Last update"

    def updates_log_display(self, obj):
        if not obj.updates_log:
            return "No updates yet"
        rows = []
        for block in reversed(obj.updates_log):
            val = block.value
            ts = val.get("at")
            if ts:
                try:
                    ts = timezone.localtime(ts).strftime("%Y-%m-%d %H:%M")
                except Exception:
                    ts = str(ts)
            rows.append((ts or "—", val.get("by") or "—", val.get("note") or ""))
        return format_html(
            "<table style='border-collapse:collapse;width:100%;font-family:monospace;'>"
            "<thead><tr>"
            "<th style='text-align:left;padding:4px;border-bottom:1px solid #ccc;'>When</th>"
            "<th style='text-align:left;padding:4px;border-bottom:1px solid #ccc;'>Who</th>"
            "<th style='text-align:left;padding:4px;border-bottom:1px solid #ccc;'>Note</th>"
            "</tr></thead><tbody>{}</tbody></table>",
            format_html_join(
                "",
                "<tr>"
                "<td style='padding:4px;border-bottom:1px solid #eee;'>{0}</td>"
                "<td style='padding:4px;border-bottom:1px solid #eee;'>{1}</td>"
                "<td style='padding:4px;border-bottom:1px solid #eee;'>{2}</td>"
                "</tr>",
                rows,
            ),
        )

    updates_log_display.short_description = "Change Log"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        """Append a comment-only log entry; keep all fields read-only for integrity."""
        comment = form.cleaned_data.get("add_comment") if hasattr(form, "cleaned_data") else None
        if comment:
            entry = {
                "at": timezone.now(),
                "by": getattr(getattr(request, "user", None), "username", ""),
                "note": f"Comment: {comment}",
            }
            new_value = list(obj.updates_log) if obj.updates_log else []
            new_value.append({"type": "update", "value": entry})
            obj.updates_log = new_value
            obj.save(update_fields=["updates_log"])

from django.contrib import admin
from django.utils.html import format_html
from .models import BrandDiscoverySubmission, BrandDiscoveryPage

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
        
        # Build a mapping from field keys (e.g., question_1_1) to readable labels
        label_map = {}
        try:
            page = BrandDiscoveryPage.objects.live().first() or BrandDiscoveryPage.objects.first()
            if page and page.form_sections:
                for s_idx, section_block in enumerate(page.form_sections, start=1):
                    section = section_block.value
                    section_title = section.get('section_title') or f'Section {s_idx}'
                    questions = section.get('questions') or []
                    for q_idx, question in enumerate(questions, start=1):
                        key = f"question_{s_idx}_{q_idx}"
                        label = question.get('label') if hasattr(question, 'get') else getattr(question, 'label', None)
                        if not label and hasattr(question, 'value'):
                            # In case of StructValue
                            label = question.value.get('label')
                        label_map[key] = {
                            'label': label or f'Question {s_idx}.{q_idx}',
                            'section': section_title,
                        }
        except Exception:
            # If any issue, fall back to raw keys
            label_map = {}

        html = '<div style="padding: 15px; border-radius: 8px;">'
        
        for key, value in obj.additional_responses.items():
            # Prefer mapped label from page definition
            if key in label_map:
                formatted_key = f"{label_map[key]['section']} — {label_map[key]['label']}"
            else:
                # Fallback: prettify the raw key
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
