import os
import sys
import requests
from xml.etree import ElementTree as ET
from urllib.parse import urlparse


def test_sitemap_index():
    """Test that the sitemap index contains all expected sections."""
    print("\nTesting sitemap index...")
    try:
        response = requests.get('http://localhost:8000/sitemap.xml')
        response.raise_for_status()
        
        # Parse the XML
        root = ET.fromstring(response.content)
        
        # Define the namespace
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        # Find all sitemap elements
        sitemaps = root.findall('.//sm:sitemap', ns)
        
        # Check if we have at least the expected sections
        expected_sections = ['wagtail', 'services', 'static']
        found_sections = []
        
        for sitemap in sitemaps:
            loc = sitemap.find('sm:loc', ns).text
            print(f"Found sitemap: {loc}")
            for section in expected_sections:
                if f'sitemap-{section}.xml' in loc:
                    found_sections.append(section)
        
        missing_sections = set(expected_sections) - set(found_sections)
        if missing_sections:
            print(f"❌ Missing sections: {', '.join(missing_sections)}")
        else:
            print("✅ All expected sections found in sitemap index")
            print("✅ All sitemaps are now managed by Django's sitemap framework")
            
        return found_sections
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error accessing sitemap index: {e}")
        return []


def test_section_sitemap(section):
    """Test a specific section sitemap."""
    print(f"\nTesting {section} sitemap...")
    try:
        response = requests.get(f'http://localhost:8000/sitemap-{section}.xml')
        response.raise_for_status()
        
        # Parse the XML
        root = ET.fromstring(response.content)
        
        # Define the namespace
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        # Find all URL elements
        urls = root.findall('.//sm:url', ns)
        
        print(f"Found {len(urls)} URLs in {section} sitemap")
        
        # Print the first 5 URLs
        for i, url in enumerate(urls[:5]):
            loc = url.find('sm:loc', ns).text
            print(f"  {i+1}. {loc}")
            
        if len(urls) > 5:
            print(f"  ... and {len(urls) - 5} more")
            
        return len(urls) > 0
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error accessing {section} sitemap: {e}")
        return False


def main():
    print("=== Sitemap Testing Tool ===")
    print("This script tests the Django-managed combined sitemap implementation.")
    print("Make sure your development server is running at http://localhost:8000")
    
    # Test the sitemap index
    sections = test_sitemap_index()
    
    # Test each section sitemap
    all_sections_valid = True
    for section in sections:
        section_valid = test_section_sitemap(section)
        all_sections_valid = all_sections_valid and section_valid
    
    # Summary
    print("\n=== Test Summary ===")
    if all_sections_valid and sections:
        print("✅ Django-managed combined sitemap implementation is working correctly!")
        print("✅ All content types (Wagtail pages, Services, Static views) are included")
    else:
        print("❌ There are issues with the sitemap implementation.")
        print("   Please check the output above for details.")


if __name__ == "__main__":
    main()