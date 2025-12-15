# Sitemap Implementation & Submission Guide

## Overview

This document explains the TFuture website's sitemap implementation and how to submit it to search engines for better indexing and visibility.

## Current Implementation

### Django-Managed Combined Sitemap

The TFuture website uses Django's sitemap framework to create a unified sitemap that includes:

- **Wagtail CMS Pages**: All published blog posts, projects, and products pages
- **Django Services**: All visible services from Django admin
- **Static Pages**: Core pages like home, about, and terms

### Technical Details

Implementation is in `core/sitemaps.py` with three custom sitemap classes:

1. **WagtailPageSitemap**: All published Wagtail CMS pages
2. **ServiceSitemap**: All visible services from Django admin
3. **StaticViewSitemap**: Static pages (home, about, terms)

### Sitemap Structure

- **Sitemap Index**: `/sitemap.xml` - Lists all section sitemaps
- **Section Sitemaps**:
  - `/sitemap-wagtail.xml` - All CMS pages
  - `/sitemap-services.xml` - All services
  - `/sitemap-static.xml` - Static pages

### URL Patterns

- **Wagtail Pages**: Uses Wagtail's built-in URL structure
- **Services**: Currently uses `/#service-{slug}` (anchor links on home page)
- **Static Pages**: Uses core URL patterns (`/`, `/about/`, `/terms/`)

### Configuration

Located in `TFuture/urls.py`:

```python
path('sitemap.xml', sitemap_index_view, {
    'sitemaps': {
        'wagtail': WagtailPageSitemap,
        'services': ServiceSitemap,
        'static': StaticViewSitemap,
    },
    'sitemap_url_name': 'django.contrib.sitemaps.views.sitemap'
}),
```

## Customization

### Modifying Service URLs

If your service URL structure changes, update the `location` method in `ServiceSitemap` class:

```python
# For dedicated service pages
def location(self, obj):
    return f'/services/{obj.slug}/'

# For anchor links (current)
def location(self, obj):
    return f'/#service-{obj.slug}'
```

### Adding More Models

To add additional Django models to the sitemap:

1. Create a new sitemap class in `core/sitemaps.py`
2. Add it to the `sitemaps` dictionary in `TFuture/urls.py`

Example:

```python
class TestimonialSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Testimonial.objects.filter(featured=True)

    def lastmod(self, obj):
        return obj.updated_at
```

## Testing Your Sitemap

### Local Testing

1. Start the development server: `python manage.py runserver`
2. Visit `http://localhost:8000/sitemap.xml` to see the sitemap index
3. Click on section links to view individual sitemaps
4. Verify all expected URLs are included

### Online Validation

Before submission, validate your sitemap:

- [XML Sitemap Validator](https://www.xml-sitemaps.com/validate-xml-sitemap.html)
- [Google's Rich Results Test](https://search.google.com/test/rich-results)

## Submitting to Google Search Console

### Step 1: Verify Website Ownership

1. Go to [Google Search Console](https://search.google.com/search-console/about)
2. Click "Start now"
3. Enter your website URL (use domain property type for best results)
4. Verify ownership using one of these methods:
   - **HTML file upload**: Upload verification file to your server
   - **HTML tag**: Add meta tag to your site's homepage
   - **DNS record**: Add TXT record to your domain's DNS
   - **Google Analytics**: If already installed
   - **Google Tag Manager**: If already installed

### Step 2: Submit Sitemap

1. In Google Search Console, select your verified property
2. Navigate to **Sitemaps** in the left sidebar
3. Enter `sitemap.xml` in the "Add a new sitemap" field
4. Click **Submit**

### Step 3: Monitor Indexing

1. Google processes the sitemap and begins indexing pages
2. Monitor status in the Sitemaps report
3. Check for errors or warnings
4. Verify pages appear in Coverage report

## Submitting to Other Search Engines

### Bing Webmaster Tools

1. Go to [Bing Webmaster Tools](https://www.bing.com/webmasters)
2. Verify site ownership
3. Submit sitemap at `https://yourdomain.com/sitemap.xml`

### Yandex Webmaster

1. Visit [Yandex Webmaster](https://webmaster.yandex.com/)
2. Add and verify your site
3. Submit sitemap in the indexing section

## Automatic Updates

The sitemap automatically updates when:

- New Wagtail pages are published
- Services are added/removed or visibility changes
- Pages are unpublished or deleted

No manual intervention required - Django regenerates sitemaps on each request.

## Troubleshooting

### Common Issues

**Sitemap Not Found (404)**
- Verify server is running
- Check `TFuture/urls.py` configuration
- Ensure `django.contrib.sitemaps` is in `INSTALLED_APPS`

**Pages Not Indexed**
- Check for `noindex` meta tags
- Verify `robots.txt` isn't blocking pages
- Ensure pages are publicly accessible

**Errors in Search Console**
- Review error details in Search Console
- Validate sitemap XML syntax
- Check for broken URLs

### Verification

Check your sitemap is working:

```bash
# Test sitemap index
curl http://localhost:8000/sitemap.xml

# Test section sitemaps
curl http://localhost:8000/sitemap-wagtail.xml
curl http://localhost:8000/sitemap-services.xml
curl http://localhost:8000/sitemap-static.xml
```

## Best Practices

1. ✅ **Keep updated**: Django handles this automatically
2. ✅ **Submit after major changes**: New content sections or restructuring
3. ✅ **Monitor regularly**: Check Search Console weekly
4. ✅ **Fix errors promptly**: Address issues as they appear
5. ✅ **Use appropriate priorities**: Already configured in sitemap classes
6. ✅ **Include all important pages**: Verify nothing critical is missing

## Additional Resources

- [Google Sitemap Documentation](https://developers.google.com/search/docs/advanced/sitemaps/overview)
- [Django Sitemap Framework](https://docs.djangoproject.com/en/stable/ref/contrib/sitemaps/)
- [Wagtail Documentation](https://docs.wagtail.org/en/stable/reference/contrib/sitemaps.html)
- [Google Search Console Help](https://support.google.com/webmasters/)

---

**Related Files:**
- `core/sitemaps.py` - Sitemap class definitions
- `TFuture/urls.py` - Sitemap URL configuration
- `robots.txt` - Search engine crawler instructions
