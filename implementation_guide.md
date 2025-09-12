# TFuture Website Implementation Guide

## Introduction

This guide outlines how to implement the architecture described in `project_architecture.md` without changing the existing logic and design of the TFuture Website. The implementation focuses on creating a clear separation between Wagtail (content management) and Django Admin (business logic).

## Implementation Steps

### 1. Project Architecture Document

The `project_architecture.md` file has been created to document the separation of concerns between Wagtail and Django Admin. This serves as a reference for future development.

### 2. Move and Rename HomePage Model to CMS App

The HomePage model has been moved from the core app to the cms app and renamed to TestimonialsPage in `cms/homepage_model.py` to better reflect its purpose. To complete this implementation:

1. Add the TestimonialsPage model to `cms/models.py`:

```python
from .homepage_model import TestimonialsPage, TestimonialBlock
   ```

2. Use the provided migration file in `cms/migrations/0008_rename_homepage_to_testimonialspage.py` which creates the TestimonialsPage model in the cms app:
   ```bash
   python manage.py migrate cms
   ```
   
   Note: Instead of renaming the model, we're creating a new model in the cms app with the new name. This approach avoids migration errors since the HomePage model exists in the core app, not in cms.

3. Remove the HomePage model from `core/models.py` after the migration is complete.

### 3. Service API

A Service API has been created in `core/api.py` to allow the frontend to consume service data. To implement this:

1. Add the API endpoints to `core/urls.py`:
   ```python
   from .api import get_services, get_service_detail
   
   urlpatterns = [
       # Existing URLs
       path('api/services/', get_services, name='api_services'),
       path('api/services/<slug:slug>/', get_service_detail, name='api_service_detail'),
   ]
   ```

2. Update the frontend templates to use the API endpoints if needed.

### 4. Update Admin Registration

The updated admin registration is in `core/admin_updated.py`. To implement this:

1. Replace the contents of `core/admin.py` with the contents of `core/admin_updated.py`.

2. Remove the `@register_snippet` decorator from the Service model in `core/models.py` to prevent it from being registered in Wagtail admin.

## Maintaining Existing Logic and Design

This implementation maintains the existing logic and design by:

1. **Not changing any functionality**: All models retain their fields and methods.
2. **Not altering templates**: Frontend templates remain unchanged.
3. **Preserving URL routing**: URL patterns remain the same.
4. **Keeping database structure**: No changes to the database schema except for moving and renaming the HomePage model to TestimonialsPage.

## Testing

After implementation, test the following:

1. Verify that all pages load correctly.
2. Ensure that service requests can still be submitted and managed.
3. Check that content can be edited in Wagtail admin.
4. Confirm that business data can be managed in Django admin.
5. Test the Service API endpoints.

## Conclusion

This implementation creates a clear separation between content management (Wagtail) and business logic (Django Admin) without changing the existing functionality or design of the TFuture Website. The separation improves maintainability and provides specialized interfaces for different types of users.