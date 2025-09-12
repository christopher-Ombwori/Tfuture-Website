# 🚀 Brevo API Email Setup Guide

## Overview
This guide explains how to use the Brevo API for sending transactional emails in your TFuture website. We've replaced the previous SMTP implementation with a more reliable API-based approach.

## What We've Implemented

### ✨ Features:
1. **Admin Notification Email** - You'll receive a notification when someone submits a service request
2. **Customer Confirmation Email** - Customers get a confirmation email with next steps
3. **API-based Delivery** - More reliable than SMTP, bypasses port 25 restrictions
4. **Error Handling** - Comprehensive error handling and logging
5. **Message Tracking** - Each email gets a unique message ID for tracking

## Setup Instructions

### 1. Get Your Brevo API Key
1. Go to [Brevo.com](https://www.brevo.com) and create an account
2. Navigate to Settings → API Keys
3. Generate a new API key with appropriate permissions (at minimum: "SMTP")
4. Copy your API key

### 2. Configure Environment Variables
Add this to your `.env` file:

```env
# Email Settings (Brevo API)
DEFAULT_FROM_EMAIL=contact@tfuturedesigns.studio
DEFAULT_FROM_NAME=TFuture
ADMIN_EMAIL=contact@tfuturedesigns.studio
CONTACT_EMAIL=contact@tfuturedesigns.studio
SITE_URL=http://localhost:8000
BREVO_API_KEY=your-brevo-api-key-here
```

### 3. Update Email Addresses
Replace the placeholder values with your actual information:
- `DEFAULT_FROM_EMAIL`: The email address that will appear as the sender
- `DEFAULT_FROM_NAME`: The name that will appear as the sender
- `ADMIN_EMAIL`: Your email address where you want to receive notifications
- `SITE_URL`: Your website URL (for admin panel links)
- `BREVO_API_KEY`: Your Brevo API key

### 4. Test the Setup
1. Run the test script: `python test_brevo_api.py`
2. Check your email for the test message
3. If successful, submit a service request through your website
4. Verify both admin and customer emails are received

## How It Works

### 🔄 Email Flow:
1. Customer submits service request form
2. Request is saved to database
3. `send_service_request_emails()` is called from views.py
4. Both admin notification and customer confirmation emails are sent via Brevo API
5. Success message is shown to customer

### 📊 API Response:
Each email send attempt returns a response with:
- `success`: Boolean indicating if the email was sent successfully
- `message_id`: Unique ID for the email (if successful)
- `status_code`: HTTP status code from the API
- `error`: Error message (if unsuccessful)

## Troubleshooting

### Common Issues:

1. **API Key Issues**
   - Verify your Brevo API key is correct
   - Check that your API key has the necessary permissions
   - Ensure the API key is properly set in your .env file

2. **Email Not Received**
   - Check spam/junk folders
   - Verify recipient email addresses are correct
   - Check logs for any API errors

3. **API Errors**
   - Check your Brevo account limits
   - Verify sender domain is properly set up in Brevo
   - Check for any API rate limiting issues

### Debug Mode:
The system logs all email activities. Check your Django logs for detailed information about email sending status.

## Customization

### Email Templates:
You can customize the email templates in:
- `templates/core/emails/admin_notification.html`
- `templates/core/emails/customer_confirmation.html`

### Email Content:
Modify the email utility functions in `core/brevo_api.py` to change:
- Email subjects
- Content structure
- Sender information

## Security Notes

- Never commit your `.env` file to version control
- Keep your Brevo API key secure
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

🎉 **Congratulations!** Your Brevo API email system is now ready to send professional, automated email notifications!