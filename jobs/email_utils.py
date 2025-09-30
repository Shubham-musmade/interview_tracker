from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
import os


def send_application_email(application, subject, message, to_email, cc_email=None, 
                          attach_resume=True, attach_cover_letter=True):
    """
    Send a job application email with attachments
    
    Args:
        application: JobApplication instance
        subject: Email subject
        message: Email body
        to_email: Recipient email
        cc_email: CC email (optional)
        attach_resume: Whether to attach resume
        attach_cover_letter: Whether to attach cover letter
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Create email message
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
            cc=[cc_email] if cc_email else [],
        )
        
        # Attach resume if requested and available
        if attach_resume and application.resume and application.resume.file:
            if os.path.exists(application.resume.file.path):
                email.attach_file(application.resume.file.path)
        
        # Attach cover letter if requested and available
        if attach_cover_letter and application.cover_letter and application.cover_letter.file:
            if os.path.exists(application.cover_letter.file.path):
                email.attach_file(application.cover_letter.file.path)
        
        # Send email
        email.send()
        
        # Mark application as sent
        application.mark_as_sent()
        
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False


def send_interview_reminder_email(interview_round):
    """
    Send an interview reminder email
    
    Args:
        interview_round: InterviewRound instance
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        application = interview_round.application
        user = application.user
        
        subject = f"Interview Reminder: {application.position.title} at {application.position.company.name}"
        
        # Create email content
        context = {
            'user': user,
            'application': application,
            'interview_round': interview_round,
        }
        
        message = render_to_string('jobs/emails/interview_reminder.txt', context)
        
        # Send email to user
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        
        email.send()
        return True
        
    except Exception as e:
        print(f"Error sending interview reminder: {str(e)}")
        return False


def send_status_update_notification(application, old_status, new_status):
    """
    Send notification when application status changes
    
    Args:
        application: JobApplication instance
        old_status: Previous status
        new_status: New status
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        user = application.user
        
        if not user.email:
            return False
            
        subject = f"Status Update: {application.position.title} at {application.position.company.name}"
        
        # Create email content
        context = {
            'user': user,
            'application': application,
            'old_status': old_status,
            'new_status': new_status,
        }
        
        message = render_to_string('jobs/emails/status_update.txt', context)
        
        # Send email to user
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        
        email.send()
        return True
        
    except Exception as e:
        print(f"Error sending status update notification: {str(e)}")
        return False


def send_deadline_reminder_email(applications):
    """
    Send deadline reminder emails for applications
    
    Args:
        applications: List of JobApplication instances with approaching deadlines
    
    Returns:
        int: Number of emails sent successfully
    """
    sent_count = 0
    
    for application in applications:
        try:
            user = application.user
            
            if not user.email:
                continue
                
            subject = f"Application Deadline Reminder: {application.position.title}"
            
            # Create email content
            context = {
                'user': user,
                'application': application,
            }
            
            message = render_to_string('jobs/emails/deadline_reminder.txt', context)
            
            # Send email to user
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            
            email.send()
            sent_count += 1
            
        except Exception as e:
            print(f"Error sending deadline reminder to {application.user.username}: {str(e)}")
            continue
    
    return sent_count


def validate_email_settings():
    """
    Validate email configuration settings
    
    Returns:
        tuple: (is_valid, error_message)
    """
    required_settings = [
        'EMAIL_HOST',
        'EMAIL_HOST_USER',
        'EMAIL_HOST_PASSWORD',
        'DEFAULT_FROM_EMAIL'
    ]
    
    for setting in required_settings:
        if not getattr(settings, setting, None):
            return False, f"Missing email setting: {setting}"
    
    return True, "Email settings are valid"


def get_email_template_context(application):
    """
    Get common context variables for email templates
    
    Args:
        application: JobApplication instance
    
    Returns:
        dict: Context dictionary for email templates
    """
    return {
        'user': application.user,
        'application': application,
        'position': application.position,
        'company': application.position.company,
        'user_name': application.user.get_full_name() or application.user.username,
        'company_name': application.position.company.name,
        'position_title': application.position.title,
        'current_date': timezone.now().date(),
    }