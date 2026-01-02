# Email Templates Documentation

## Overview
TFuture uses **MJML framework** to generate email-client compatible HTML templates. MJML compiles to bulletproof HTML with inline styles and table-based layouts that work across Gmail, Outlook, and Apple Mail.

## File Structure
```
templates/core/emails/
├── mjml/                          # Source MJML files (edit these)
│   ├── brand_discovery_customer_confirmation.mjml
│   ├── brand_discovery_admin_notification.mjml
│   ├── customer_confirmation.mjml
│   └── admin_notification.mjml
├── *.html                         # Compiled HTML files (don't edit directly)
├── clean_html.py                  # Post-processing cleanup script
└── README.md                      # This file
```

## Email Templates

### Customer-Facing Templates (with footer)
1. **brand_discovery_customer_confirmation.mjml**
   - Sent to: Customer after brand discovery form submission
   - Subject: "Brand Discovery Form Submission Confirmation - TFuture"
   - Variables: `{{ business_name }}`, `{{ rep_name }}`
   - Features: Success icon, footer with logo + social icons

2. **customer_confirmation.mjml**
   - Sent to: Customer after service request submission
   - Subject: "Service Request Confirmation - TFuture"
   - Variables: `{{ first_name }}`, `{{ last_name }}`, `{{ service_name }}`, `{{ request_id }}`, `{{ created_at }}`, `{{ message }}`
   - Features: Success icon, request details table, footer with logo + social icons

### Admin Templates (no footer)
3. **brand_discovery_admin_notification.mjml**
   - Sent to: Admin when brand discovery form is submitted
   - Subject: "New Brand Discovery Inquiry: {business_name} - {rep_name}"
   - Variables: `{{ business_name }}`, `{{ rep_name }}`, `{{ email }}`, `{{ phone }}`, `{{ created_at }}`, `{{ submission_id }}`, `{% if additional_responses %}`
   - Features: Bullseye emoji 🎯, contact info table, admin button

4. **admin_notification.mjml**
   - Sent to: Admin when service request is submitted
   - Subject: "New Service Request: {service_name} - {first_name} {last_name}"
   - Variables: `{{ first_name }}`, `{{ last_name }}`, `{{ email }}`, `{{ phone }}`, `{{ service_name }}`, `{{ request_id }}`, `{{ created_at }}`, `{{ message }}`
   - Features: Request details, contact client button

## Brand Assets

### Logos
- **Header (Teal)**: `tfuture logo teal.png`
  - Brand Discovery Customer: 240px
  - Customer Confirmation: 200px
  - Brand Discovery Admin: 160px
  - Admin Notification: 140px
- **Footer (White)**: `tfuture logo white-02.png` - 90px (customer templates only)
- **Success Icon**: `success confirmation.png` - 96px

### Social Icons (22px, customer templates only)
- linkedin-icon.png
- instagram-icon.png
- facebook-icon.png
- tiktok-icon.png

### Color Palette
- **Header/Footer Background**: `#1d2840` (dark blue-gray)
- **Teal Accent**: `#14B8A6` (buttons, links)
- **Teal Backgrounds**: `#e0f2f1` (light), `#ecfeff` (lighter)
- **Teal Text**: `#0f766e` (headings in boxes)
- **Content Background**: `#ffffff` (white)
- **Page Background**: `#f3f4f6` (light gray)
- **Text**: `#1f2937` (body), `#374151` (secondary), `#9CA3AF` (footer)

## Image URLs
All images use **production URLs**:
```
https://www.tfuturedesigns.studio/static/images/email_images/
```

❌ **Never commit localhost URLs** (`http://localhost:8000`)

## Compilation Process

### Prerequisites
- Node.js and npm installed
- MJML installed: `npm install` (reads from package.json)

### Development (Windows)
```bash
cd templates/core/emails
npx mjml mjml/*.mjml -o .
python clean_html.py
```

### Production (Server)
```bash
cd /path/to/project
npm install                          # Install MJML
cd templates/core/emails
npx mjml mjml/*.mjml -o .           # Compile all templates
python3 clean_html.py               # Clean empty style attributes
```

Or use the script:
```bash
chmod +x compile_emails.sh
./compile_emails.sh
```

## Making Changes

### To Update Content
1. Edit the `.mjml` file in `mjml/` folder
2. Recompile: `npx mjml mjml/filename.mjml -o filename.html`
3. Run cleanup: `python clean_html.py`
4. Test the HTML file

### To Update Colors
Search and replace hex codes in MJML files:
- `#14B8A6` - Teal accent (buttons, links)
- `#1d2840` - Header/footer background
- `#e0f2f1` - Light teal boxes

### To Update Logos
1. Replace image in `static/images/email_images/`
2. Update `width` attribute in MJML `<mj-image>` tags
3. Recompile templates

### To Update Subject Lines
Edit in Python files:
- `core/brevo_api.py` (lines 93, 135, 194, 236)
- `core/brand_discovery_emails.py` (lines 32, 74)

## Important Rules

### ✅ DO:
- Always edit `.mjml` files, never `.html` files directly
- Use production URLs (`https://www.tfuturedesigns.studio`)
- Run `clean_html.py` after compiling
- Test in Gmail, Outlook, and Apple Mail
- Use PNG images (no SVG in emails)
- Keep inline styles (email clients strip external CSS)

### ❌ DON'T:
- Edit compiled `.html` files (changes will be overwritten)
- Use localhost URLs in production
- Use external CSS stylesheets
- Use SVG images
- Forget to recompile after MJML changes
- Add footers to admin templates (intentionally excluded)

## MJML Structure

### Basic Layout
```xml
<mjml>
  <mj-head>
    <mj-attributes>
      <!-- Global styles -->
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f3f4f6">
    <mj-section>              <!-- Row -->
      <mj-column>             <!-- Cell -->
        <mj-text>             <!-- Content -->
        <mj-image>
        <mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>
```

### Common Components
- `<mj-section>` - Horizontal row container
- `<mj-column>` - Vertical column within section
- `<mj-text>` - Text content (can contain raw HTML)
- `<mj-image>` - Images with responsive sizing
- `<mj-button>` - Call-to-action buttons

### Complex Layouts
For complex layouts (tables, custom styling), use raw HTML inside `<mj-text>`:
```xml
<mj-text padding="0">
  <div style="background-color:#ffffff;padding:20px;">
    <!-- Complex HTML here -->
  </div>
</mj-text>
```

## Dependencies

### Node.js (package.json)
```json
"devDependencies": {
  "mjml": "^4.18.0"
}
```

### Python (requirements.txt)
No Python packages needed for MJML. Email sending handled by:
- Django email backend
- Brevo API integration (core/brevo_api.py)

## Email Sending Logic

### Files
- `core/brevo_api.py` - Main email sending functions
- `core/brand_discovery_emails.py` - Brand discovery specific logic

### Functions
- `send_service_request_confirmation()` - Customer confirmation
- `send_service_request_admin_notification()` - Admin notification
- `send_brand_discovery_confirmation()` - Brand discovery customer
- `send_brand_discovery_admin_notification()` - Brand discovery admin

## Testing

### Test Email Rendering
1. Open compiled HTML in browser
2. Use [Litmus](https://litmus.com) or [Email on Acid](https://www.emailonacid.com) for cross-client testing
3. Send test emails through Django to real Gmail/Outlook accounts

### Common Issues
- **Images not loading**: Check URL (production vs localhost)
- **Layout broken**: Recompile MJML, ensure no external CSS
- **Footer missing**: Check template type (admin templates don't have footers)
- **Empty file after cleaning**: Run `clean_html.py` again with proper context managers

## Admin Panel Configuration
Brand discovery admin button links to:
```
https://www.tfuturedesigns.studio/my-admin-futuristic
```

Update in [brand_discovery_admin_notification.mjml](mjml/brand_discovery_admin_notification.mjml#L63) if admin URL changes.

## Quick Reference

### Compile Single Template
```bash
npx mjml mjml/customer_confirmation.mjml -o customer_confirmation.html
```

### Compile All Templates
```bash
npx mjml mjml/*.mjml -o .
```

### View Template in Browser
```bash
# Windows
start customer_confirmation.html

# Linux/Mac
open customer_confirmation.html
```

### Check for Localhost URLs
```bash
grep -r "localhost:8000" *.html
```

## Support
For MJML documentation: https://mjml.io/documentation/

For questions about TFuture email templates, contact the development team.
