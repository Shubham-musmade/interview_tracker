# Email Configuration Guide for Interview Tracker

This guide will help you configure email settings for the Interview Tracker application to send professional emails to HR with resume and cover letter attachments.

## 📧 Email Configuration Steps

### 1. Update Django Settings

The email settings are already configured in `interview_tracker/settings.py`. Update the following values:

```python
# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Change for other providers
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'  # Your email address
EMAIL_HOST_PASSWORD = 'your-app-password'  # Your email password or app password
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'  # Default sender email
```

### 2. Gmail Configuration

For Gmail users:

1. **Enable 2-Factor Authentication** on your Google account
2. **Generate App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
   - Use this app password in `EMAIL_HOST_PASSWORD`

### 3. Other Email Providers

#### Outlook/Hotmail
```python
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

#### Yahoo Mail
```python
EMAIL_HOST = 'smtp.mail.yahoo.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

#### Custom SMTP
```python
EMAIL_HOST = 'your-smtp-server.com'
EMAIL_PORT = 587  # or 465 for SSL
EMAIL_USE_TLS = True  # or EMAIL_USE_SSL = True for port 465
```

### 4. Environment Variables (Recommended)

For security, use environment variables:

1. Create a `.env` file in your project root:
```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

2. Update `settings.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
```

3. Install python-dotenv:
```bash
pip install python-dotenv
```

## 🚀 Features Added

### 1. Professional Email Template
- **HTML Email Template**: Beautiful, responsive HTML email template
- **Plain Text Fallback**: Text version for email clients that don't support HTML
- **Professional Design**: Clean, modern design with company branding
- **Mobile Responsive**: Works well on all devices

### 2. Enhanced Email Form
- **HR Contact Information**: Fields for HR name and email
- **Personal Message**: Custom message field for personalization
- **Document Management**: Smart attachment handling
- **Email Preview**: Preview functionality before sending
- **Validation**: Ensures at least one document is attached

### 3. Smart Document Handling
- **Automatic Detection**: Detects available resume and cover letter
- **File Validation**: Ensures files exist before attaching
- **Document Status**: Shows which documents are available/missing
- **Easy Upload**: Quick links to document management

### 4. User Interface Improvements
- **Application Detail Page**: Comprehensive application details with action buttons
- **List View Updates**: Enhanced application list with email options
- **Professional Styling**: Modern, clean interface design
- **Status Indicators**: Visual indicators for email status

## 📝 How to Use

### 1. Upload Documents
1. Go to **Documents** section
2. Upload your resume (PDF/DOC/DOCX)
3. Upload your cover letter (PDF/DOC/DOCX)
4. Mark documents as default if needed

### 2. Create Job Application
1. Create or select a company
2. Add job position details
3. Fill in HR contact information
4. Attach resume and cover letter

### 3. Send Professional Email
1. Go to application details
2. Click **"Send Professional Email to HR"**
3. Fill in HR contact details
4. Add personal message (optional)
5. Preview email before sending
6. Send email with attachments

## 🔧 Troubleshooting

### Common Issues

1. **Email not sending**:
   - Check email credentials
   - Verify SMTP settings
   - Check firewall/network restrictions

2. **Gmail authentication failed**:
   - Enable 2-factor authentication
   - Use app-specific password
   - Check "Less secure app access" (not recommended)

3. **Attachments not working**:
   - Verify file paths exist
   - Check file permissions
   - Ensure MEDIA_ROOT is configured

4. **Template not loading**:
   - Check template file paths
   - Verify template syntax
   - Check Django template settings

### Testing Email Configuration

Add this to your Django shell for testing:
```python
from django.core.mail import send_mail

send_mail(
    'Test Email',
    'This is a test email.',
    'your-email@gmail.com',
    ['recipient@example.com'],
    fail_silently=False,
)
```

## 📚 Additional Features

### Future Enhancements
- Email scheduling
- Email templates library
- Email tracking and analytics
- Bulk email sending
- Email signature management
- Integration with calendar for follow-ups

### Security Best Practices
- Use environment variables for sensitive data
- Enable 2-factor authentication
- Use app-specific passwords
- Regularly rotate credentials
- Monitor email sending logs

## 📞 Support

If you encounter any issues:
1. Check the error logs in Django admin
2. Verify email provider settings
3. Test with a simple email first
4. Check network connectivity

The email functionality is now fully integrated into your Interview Tracker application!