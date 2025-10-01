from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserEmail(models.Model):
    """Model to store multiple email addresses for a user"""
    EMAIL_TYPE_CHOICES = [
        ('PERSONAL', 'Personal'),
        ('PROFESSIONAL', 'Professional'),
        ('ACADEMIC', 'Academic'),
        ('OTHER', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_emails')
    email = models.EmailField()
    email_type = models.CharField(max_length=20, choices=EMAIL_TYPE_CHOICES, default='PROFESSIONAL')
    label = models.CharField(max_length=100, help_text="e.g., 'Work Gmail', 'University Email'")
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_primary', 'email_type', 'label']
        unique_together = ['user', 'email']

    def __str__(self):
        return f"{self.label} ({self.email})"

    def save(self, *args, **kwargs):
        # If this is set as primary, unset other primary emails for this user
        if self.is_primary:
            UserEmail.objects.filter(user=self.user, is_primary=True).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)


class Company(models.Model):
    """Model to store company information"""
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ['name']

    def __str__(self):
        return self.name


class JobPosition(models.Model):
    """Model to store job position details"""
    EMPLOYMENT_TYPE_CHOICES = [
        ('FULL_TIME', 'Full Time'),
        ('PART_TIME', 'Part Time'),
        ('CONTRACT', 'Contract'),
        ('FREELANCE', 'Freelance'),
        ('INTERNSHIP', 'Internship'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='positions')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    requirements = models.TextField(blank=True, null=True)
    employment_type = models.CharField(
        max_length=20, 
        choices=EMPLOYMENT_TYPE_CHOICES, 
        default='FULL_TIME'
    )
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    remote_allowed = models.BooleanField(default=False)
    job_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} at {self.company.name}"


class Document(models.Model):
    """Model to store resumes and cover letters"""
    DOCUMENT_TYPE_CHOICES = [
        ('RESUME', 'Resume'),
        ('COVER_LETTER', 'Cover Letter'),
        ('PORTFOLIO', 'Portfolio'),
        ('OTHER', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    name = models.CharField(max_length=200)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    file = models.FileField(upload_to='documents/%Y/%m/')
    description = models.TextField(blank=True, null=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_document_type_display()})"

    def save(self, *args, **kwargs):
        # If this document is set as default, unset other defaults of the same type
        if self.is_default:
            Document.objects.filter(
                user=self.user, 
                document_type=self.document_type, 
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)


class JobApplication(models.Model):
    """Model to track job applications"""
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('APPLIED', 'Applied'),
        ('PHONE_SCREEN', 'Phone Screen'),
        ('TECHNICAL_INTERVIEW', 'Technical Interview'),
        ('ONSITE_INTERVIEW', 'Onsite Interview'),
        ('FINAL_INTERVIEW', 'Final Interview'),
        ('OFFER_RECEIVED', 'Offer Received'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
        ('WITHDRAWN', 'Withdrawn'),
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]

    PLATFORM_CHOICES = [
        ('LINKEDIN', 'LinkedIn'),
        ('INDEED', 'Indeed'),
        ('GLASSDOOR', 'Glassdoor'),
        ('COMPANY_WEBSITE', 'Company Website'),
        ('JOBBOARD', 'Job Board'),
        ('RECRUITER', 'Recruiter Contact'),
        ('REFERRAL', 'Employee Referral'),
        ('CAREER_FAIR', 'Career Fair'),
        ('DIRECT_EMAIL', 'Direct Email'),
        ('OTHER', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    position = models.ForeignKey(JobPosition, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    
    # Application source tracking
    application_platform = models.CharField(
        max_length=20, 
        choices=PLATFORM_CHOICES, 
        blank=True, 
        null=True,
        help_text="Platform or method used to apply for this job"
    )
    platform_url = models.URLField(
        blank=True, 
        null=True,
        help_text="Direct link to job posting if applied online"
    )
    
    # Contact information
    hr_email = models.EmailField(blank=True, null=True)
    hr_name = models.CharField(max_length=200, blank=True, null=True)
    hr_phone = models.CharField(max_length=20, blank=True, null=True)
    recruiter_email = models.EmailField(blank=True, null=True)
    recruiter_name = models.CharField(max_length=200, blank=True, null=True)
    
    # Application details
    applied_date = models.DateField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    resume = models.ForeignKey(
        Document, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='resume_applications',
        limit_choices_to={'document_type': 'RESUME'}
    )
    cover_letter = models.ForeignKey(
        Document, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='cover_letter_applications',
        limit_choices_to={'document_type': 'COVER_LETTER'}
    )
    
    # Additional information
    notes = models.TextField(blank=True, null=True)
    salary_expectation = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Email tracking
    sender_email = models.ForeignKey(
        UserEmail,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_applications',
        help_text="Email address used to send the application"
    )
    email_sent = models.BooleanField(default=False)
    email_sent_date = models.DateTimeField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'position']

    def __str__(self):
        return f"{self.user.username} - {self.position.title} at {self.position.company.name}"

    def mark_as_sent(self):
        """Mark the application as sent via email"""
        self.email_sent = True
        self.email_sent_date = timezone.now()
        if self.status == 'DRAFT':
            self.status = 'APPLIED'
            self.applied_date = timezone.now().date()
        self.save()


class InterviewRound(models.Model):
    """Model to track interview rounds for each application"""
    INTERVIEW_TYPE_CHOICES = [
        ('PHONE', 'Phone Screen'),
        ('VIDEO', 'Video Call'),
        ('TECHNICAL', 'Technical Interview'),
        ('BEHAVIORAL', 'Behavioral Interview'),
        ('ONSITE', 'Onsite Interview'),
        ('PANEL', 'Panel Interview'),
        ('PRESENTATION', 'Presentation'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('RESCHEDULED', 'Rescheduled'),
    ]

    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='interview_rounds')
    round_number = models.PositiveIntegerField()
    interview_type = models.CharField(max_length=20, choices=INTERVIEW_TYPE_CHOICES)
    interviewer_name = models.CharField(max_length=200, blank=True, null=True)
    interviewer_email = models.EmailField(blank=True, null=True)
    scheduled_date = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    location = models.CharField(max_length=200, blank=True, null=True)  # Or meeting link
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    feedback = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['application', 'round_number']
        unique_together = ['application', 'round_number']

    def __str__(self):
        return f"Round {self.round_number} - {self.get_interview_type_display()} for {self.application}"


class ApplicationNote(models.Model):
    """Model to store timestamped notes for applications"""
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='application_notes')
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Note for {self.application} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
