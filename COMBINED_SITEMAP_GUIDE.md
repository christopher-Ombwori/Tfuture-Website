# Django-Managed Combined Sitemap Guide

## Overview

This document explains the implementation of a combined sitemap.xml for the TFuture website that includes both Wagtail CMS pages and Django models, all managed through Django's sitemap framework. This approach provides comprehensive search engine indexing for all content types while maintaining a single, consistent implementation.

## Implementation Details

### 1. Custom Sitemap Classes

We've created custom sitemap classes in `core/sitemaps.py`:

- **WagtailPageSitemap**: Includes all published Wagtail CMS pages
- **ServiceSitemap**: Includes all visible services from the Django admin
- **StaticViewSitemap**: Includes static pages like home, about, and terms

### 2. Combined Sitemap Configuration

The main `TFuture/urls.py` file has been updated to create a sitemap index that includes:

- **Wagtail Pages**: All published pages from the Wagtail CMS (now managed by Django's sitemap framework)
- **Services**: All visible services from the Django admin
- **Static Views**: Core static pages like home, about, and terms

Unlike the previous implementation that used Wagtail's built-in sitemap functionality, this approach uses Django's sitemap framework for all content types, providing a more consistent and unified implementation.

### 3. Sitemap Structure

The implementation creates:

- A sitemap index at `/sitemap.xml` that references section-specific sitemaps
- Individual section sitemaps at `/sitemap-wagtail.xml`, `/sitemap-services.xml`, and `/sitemap-static.xml`

## How It Works

1. When a search engine requests `/sitemap.xml`, it receives an index listing all section sitemaps
2. The search engine then requests each section sitemap individually
3. Each section sitemap contains URLs specific to that content type

## URL Patterns

- **Wagtail Pages**: Uses Wagtail's built-in URL structure
- **Services**: Uses `/services/{slug}/` pattern
- **Static Views**: Uses core URL patterns like `/`, `/about/`, `/terms/`

## Customization

### Service URLs

The `ServiceSitemap` class currently uses a URL pattern of `/services/{slug}/`. If your actual URL structure is different, update the `location` method in `ServiceSitemap` class.

Options include:

```python
# For dedicated service pages
return f'/services/{obj.slug}/'

# For anchor links on the home page
return f'/#service-{obj.slug}'

# For any other custom URL structure
return reverse('your_url_name', kwargs={'slug': obj.slug})
```

### Adding More Models

To add more Django models to the sitemap:

1. Create a new sitemap class in `core/sitemaps.py`
2. Add the new sitemap to the `sitemaps` dictionary in `TFuture/urls.py`

Example for adding a Testimonial sitemap:

```python
class TestimonialSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Testimonial.objects.filter(featured=True)

    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return f'/testimonials/{obj.id}/'
```

## Testing

To test the sitemap implementation:

1. Start the development server
2. Visit `/sitemap.xml` to see the sitemap index
3. Click on the links to view each section sitemap
4. Verify that all expected URLs are included

## Submission to Google Search Console

Follow the instructions in `SITEMAP_SUBMISSION_GUIDE.md` to submit your sitemap to Google Search Console. The only difference is that your sitemap now includes content from both Wagtail and Django.

## Troubleshooting

### Common Issues

1. **TemplateDoesNotExist Error**: Make sure you have the required template files in your templates directory:
   - `templates/sitemap_index.xml` - For the sitemap index
   - `templates/sitemap.xml` - For individual section sitemaps
2. **404 Errors in Sitemap**: Ensure all URLs in the sitemap actually exist in your application
3. **Missing Content**: Check that your sitemap classes correctly filter and include all desired content
4. **XML Errors**: Validate your sitemap using online tools to ensure proper formatting

### URL Validation

It's important to ensure that all URLs in your sitemap actually work. Test each URL pattern to confirm that it resolves to a valid page.