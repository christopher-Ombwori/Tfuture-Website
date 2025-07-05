# 🪄 Magical Email Setup Guide

## Overview
This guide will help you set up the magical email notification system using Brevo SMTP for your TFuture website.

## What We've Implemented

### ✨ Features Added:
1. **Admin Notification Email** - You'll receive a beautiful notification when someone submits a service request
2. **Customer Confirmation Email** - Customers get a professional confirmation email with next steps
3. **Beautiful Email Templates** - Responsive, branded email templates
4. **Error Handling** - Graceful handling of email failures
5. **Logging** - All email activities are logged for debugging

### 📧 Email Templates Created:
- `templates/core/emails/admin_notification.html` - Notification for you
- `templates/core/emails/customer_confirmation.html` - Confirmation for customers

## Setup Instructions

### 1. Get Your Brevo SMTP Credentials
1. Go to [Brevo.com](https://www.brevo.com) and create an account
2. Navigate to Settings → SMTP & API
3. Copy your SMTP credentials:
   - SMTP Server: `smtp-relay.brevo.com`
   - Port: `587`
   - Username: Your Brevo username/email
   - Password: Your SMTP password

### 2. Configure Environment Variables
Add these to your `.env` file:

```env
# Email Settings (Brevo SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp-relay.brevo.com
EMAIL_PORT=2525
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=your-brevo-smtp-username
EMAIL_HOST_PASSWORD=your-brevo-smtp-password
DEFAULT_FROM_EMAIL=contact@tfuturedesigns.studio
ADMIN_EMAIL=contact@tfuturedesigns.studio
CONTACT_EMAIL=contact@tfuturedesigns.studio
SITE_URL=http://localhost:8000
```

### 3. Update Email Addresses
Replace the placeholder values with your actual credentials:
- `EMAIL_HOST_USER`: Your Brevo SMTP username (e.g., 90ce94001@smtp-brevo.com)
- `EMAIL_HOST_PASSWORD`: Your Brevo SMTP password
- `DEFAULT_FROM_EMAIL`: The email address that will appear as the sender (contact@tfuturedesigns.studio)
- `ADMIN_EMAIL`: Your email address where you want to receive notifications (contact@tfuturedesigns.studio)
- `SITE_URL`: Your website URL (for admin panel links)

### 4. Test the Setup
1. Start your Django server
2. Submit a service request through your website
3. Check your email for the admin notification
4. Check the customer's email for the confirmation

## How It Works

### 🔄 Email Flow:
1. Customer submits service request form
2. Request is saved to database
3. **Admin Notification** is sent to your email
4. **Customer Confirmation** is sent to customer's email
5. Success message is shown to customer

### 📊 Email Content:

#### Admin Notification Includes:
- Customer's full contact information
- Service requested
- Customer's message
- Direct link to admin panel
- Timestamp of submission

#### Customer Confirmation Includes:
- Request details and ID
- Next steps explanation
- Contact information
- Professional branding

## Troubleshooting

### Common Issues:

1. **Emails not sending**
   - Check your Brevo SMTP credentials are correct
   - Verify your email addresses are valid
   - Check Django logs for error messages

2. **Template not found**
   - Ensure email templates are in the correct location
   - Check template syntax

3. **SMTP errors**
   - Verify your Brevo account is active
   - Check SMTP credentials
   - Ensure you have sufficient email credits

### Debug Mode:
The system logs all email activities. Check your Django logs for detailed information about email sending status.

## Customization

### Email Templates:
You can customize the email templates in:
- `templates/core/emails/admin_notification.html`
- `templates/core/emails/customer_confirmation.html`

### Email Content:
Modify the email utility functions in `core/email_utils.py` to change:
- Email subjects
- Content structure
- Sender information

## Security Notes

- Never commit your `.env` file to version control
- Keep your Brevo SMTP credentials secure
- Use environment variables for all sensitive data
- Consider rate limiting for production use

## Production Deployment

For production deployment:
1. Update `SITE_URL` to your production domain
2. Use a verified sender email address
3. Set up proper logging
4. Monitor email delivery rates
5. Consider implementing email queuing for high volume

---

🎉 **Congratulations!** Your magical email system is now ready to enchant your customers with professional, automated email notifications! 