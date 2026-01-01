"""Clean empty style attributes from compiled MJML HTML files."""
import os
import re

# List of HTML files to clean
html_files = [
    'brand_discovery_customer_confirmation.html',
    'brand_discovery_admin_notification.html',
    'admin_notification.html',
    'customer_confirmation.html'
]

def clean_empty_styles(filepath):
    """Remove empty style="" attributes from HTML file."""
    if not os.path.exists(filepath):
        print(f'❌ File not found: {filepath}')
        return False
    
    try:
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove empty style attributes
        cleaned_content = re.sub(r'\s+style=""', '', content)
        
        # Write back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        print(f'✓ Cleaned: {filepath}')
        return True
    except Exception as e:
        print(f'❌ Error cleaning {filepath}: {e}')
        return False

if __name__ == '__main__':
    print('Cleaning HTML email templates...\n')
    success_count = 0
    
    for html_file in html_files:
        if clean_empty_styles(html_file):
            success_count += 1
    
    print(f'\n{success_count}/{len(html_files)} files cleaned successfully')
