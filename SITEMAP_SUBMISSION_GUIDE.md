# Sitemap Submission Guide for TFuture Website

## Overview

This guide explains how to submit your sitemap.xml to Google Search Console to improve your website's indexing and visibility in search results.

## Current Sitemap Configuration

The TFuture website already has a sitemap.xml configured using Wagtail's built-in sitemap functionality:

1. The sitemap is available at: `http://yourdomain.com/sitemap.xml`
2. It's configured in `TFuture/urls.py` with the path: `path("sitemap.xml", wagtail_sitemaps_views.sitemap)`
3. The required app `wagtail.contrib.sitemaps` is included in `INSTALLED_APPS` in `settings.py`

## Submitting to Google Search Console

### Step 1: Verify Website Ownership

1. Go to [Google Search Console](https://search.google.com/search-console/about)
2. Click "Start now"
3. Enter your website URL (use the domain property type for best results)
4. Verify ownership using one of the provided methods:
   - HTML file upload
   - HTML tag
   - DNS record
   - Google Analytics
   - Google Tag Manager

### Step 2: Submit Your Sitemap

1. In Google Search Console, select your verified property
2. In the left sidebar, click on "Sitemaps"
3. Enter `sitemap.xml` in the "Add a new sitemap" field
4. Click "Submit"

### Step 3: Monitor Indexing

1. Google will process your sitemap and begin indexing your pages
2. You can monitor the status in the Sitemaps report
3. Check for any errors or warnings that might prevent proper indexing

## Optimizing Your Sitemap

### Current Implementation

Wagtail's sitemap generator automatically includes:

- All published pages
- Last modification dates
- Proper URL formatting

### Additional Optimization (if needed)

If you want to customize your sitemap further, you can:

1. Add `changefreq` and `priority` attributes to specific page types by extending Wagtail's sitemap functionality
2. Exclude certain pages from the sitemap
3. Create multiple sitemaps for different sections of your site

## Troubleshooting

### Common Issues

1. **Sitemap Not Found**: Ensure your server is running and the URL is accessible
2. **Pages Not Indexed**: Check for `noindex` tags or robots.txt exclusions
3. **Errors in Search Console**: Address any reported issues with your sitemap format

### Testing Your Sitemap

Before submission, verify your sitemap is valid:

1. Access it directly in your browser: `http://yourdomain.com/sitemap.xml`
2. Use online validation tools like [XML Sitemap Validator](https://www.xml-sitemaps.com/validate-xml-sitemap.html)

## Best Practices

1. Keep your sitemap up to date (Wagtail handles this automatically)
2. Submit your sitemap after significant content changes
3. Monitor indexing status regularly in Google Search Console
4. Address any errors promptly

## Additional Resources

- [Google's Sitemap documentation](https://developers.google.com/search/docs/advanced/sitemaps/overview)
- [Wagtail Sitemap documentation](https://docs.wagtail.org/en/stable/reference/contrib/sitemaps.html)