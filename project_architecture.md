# TFuture Website Project Architecture

## Overview

This document outlines the architecture of the TFuture Website, focusing on the separation between content management (Wagtail) and business logic (Django Admin). The architecture is designed to maintain a clear separation of concerns while preserving the existing functionality and design.

## Application Structure

The project consists of two main applications:

1. **Core App**: Handles business logic and service-related functionality
2. **CMS App**: Manages content through Wagtail CMS

## Separation of Concerns

### Wagtail CMS (Content Management)

Wagtail is used exclusively for content-related models and pages:

- **Blog content**: BlogIndexPage, BlogPage, BlogCategory
- **Project portfolio**: ProjectIndexPage, ProjectPage, Category
- **Products content**: ProductsPage
- **Content blocks**: Various StreamField blocks for rich content

### Django Admin (Business Logic)

Django Admin is used for business-related models and operations:

- **Service Requests**: Managing client inquiries and service requests
- **Services**: Managing available services (currently implemented as Wagtail snippets but should be moved to Django Admin)

## Model Registration

### Wagtail Registration

- All Page models are automatically registered with Wagtail
- Content-related snippets are registered using `@register_snippet`

### Django Admin Registration

- Business models are registered in `core/admin.py`
- Custom admin classes provide specialized interfaces for business operations

## Implementation Plan

To maintain a clear separation without changing the logic and design:

1. **Move and Rename HomePage to CMS App**: The HomePage model has been moved to the CMS app and renamed to TestimonialsPage to better reflect its purpose since it only manages testimonials
2. **Create Service API**: Implement an API for frontend to consume service data
3. **Update Admin Registration**: Ensure proper model registration in respective admin interfaces

## Data Flow

```
┌─────────────────┐     ┌─────────────────┐
│   Django Admin  │     │   Wagtail CMS   │
│  (Business)     │     │   (Content)     │
└────────┬────────┘     └────────┬────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│  Service Models │     │  Content Models │
│  - ServiceRequest     │  - BlogPage     │
│  - Service      │     │  - ProjectPage  │
└────────┬────────┘     └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     ▼
           ┌─────────────────┐
           │    Frontend     │
           │    Templates    │
           └─────────────────┘
```

## Benefits of This Architecture

1. **Clear Separation**: Content editors work in Wagtail, administrators in Django Admin
2. **Specialized Interfaces**: Each interface is optimized for its specific use case
3. **Maintainability**: Easier to maintain and extend functionality
4. **Security**: Better control over permissions and access

## Implementation Notes

- No changes to existing logic or design are required
- The separation is achieved through proper model registration and organization
- Frontend templates remain unchanged
- URL routing remains unchanged