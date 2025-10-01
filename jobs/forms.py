from django import forms
from django.contrib.auth.models import User
from .models import Company, JobPosition, JobApplication, Document, InterviewRound, ApplicationNote, UserEmail


class UserEmailForm(forms.ModelForm):
    class Meta:
        model = UserEmail
        fields = ['email', 'email_type', 'label', 'is_primary', 'is_active']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your.email@example.com'}),
            'email_type': forms.Select(attrs={'class': 'form-control'}),
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Work Gmail, University Email'}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.user = user
        
        if self.user:
            # Check if user has any primary email
            has_primary = UserEmail.objects.filter(user=self.user, is_primary=True).exists()
            if not has_primary:
                self.fields['is_primary'].initial = True


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'website', 'location', 'industry', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, Country'}),
            'industry': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Technology, Finance, etc.'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief description about the company...'}),
        }


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['position', 'sender_email', 'status', 'priority', 'application_platform', 'platform_url',
                 'hr_email', 'hr_name', 'hr_phone', 'recruiter_email', 'recruiter_name', 
                 'applied_date', 'deadline', 'resume', 'cover_letter', 'notes', 'salary_expectation']
        widgets = {
            'position': forms.Select(attrs={'class': 'form-control'}),
            'sender_email': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'application_platform': forms.Select(attrs={'class': 'form-control'}),
            'platform_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/jobs/...'}),
            'hr_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'hr@company.com'}),
            'hr_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'HR Contact Name'}),
            'hr_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 123-4567'}),
            'recruiter_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'recruiter@company.com'}),
            'recruiter_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Recruiter Name'}),
            'applied_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'resume': forms.Select(attrs={'class': 'form-control'}),
            'cover_letter': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Additional notes...'}),
            'salary_expectation': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Expected salary'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            # Set up sender email choices
            user_emails = UserEmail.objects.filter(user=self.user, is_active=True)
            self.fields['sender_email'].queryset = user_emails
            
            # Set primary email as initial
            primary_email = user_emails.filter(is_primary=True).first()
            if primary_email:
                self.fields['sender_email'].initial = primary_email
            elif user_emails.exists():
                self.fields['sender_email'].initial = user_emails.first()
            
            # Filter documents to only show user's documents
            self.fields['resume'].queryset = Document.objects.filter(
                user=self.user, document_type='RESUME'
            ).order_by('-is_default', '-updated_at')
            self.fields['cover_letter'].queryset = Document.objects.filter(
                user=self.user, document_type='COVER_LETTER'
            ).order_by('-is_default', '-updated_at')
            
            # Set default documents if available
            default_resume = Document.objects.filter(
                user=self.user, document_type='RESUME', is_default=True
            ).first()
            if default_resume:
                self.fields['resume'].initial = default_resume
            
            default_cover_letter = Document.objects.filter(
                user=self.user, document_type='COVER_LETTER', is_default=True
            ).first()
            if default_cover_letter:
                self.fields['cover_letter'].initial = default_cover_letter
        
        self.fields['sender_email'].empty_label = "Select sender email"
        self.fields['resume'].empty_label = "Select a resume"
        self.fields['cover_letter'].empty_label = "Select a cover letter"

    def save(self, commit=True):
        application = super().save(commit=False)
        if self.user:
            application.user = self.user
        if commit:
            application.save()
        return application


class JobPositionForm(forms.ModelForm):
    class Meta:
        model = JobPosition
        fields = ['title', 'description', 'requirements', 'employment_type', 
                 'salary_min', 'salary_max', 'location', 'remote_allowed', 'job_url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Job description...'}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Job requirements...'}),
            'employment_type': forms.Select(attrs={'class': 'form-control'}),
            'salary_min': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minimum salary'}),
            'salary_max': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Maximum salary'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job location'}),
            'remote_allowed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'job_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Job posting URL'}),
        }

    def save(self, commit=True):
        position = super().save(commit=False)
        
        # Create or get a default "Unknown Company" for positions without company
        unknown_company, created = Company.objects.get_or_create(
            name='Unknown Company',
            defaults={
                'description': 'Default company for positions without specified company',
                'website': '',
                'location': '',
                'industry': 'Unknown'
            }
        )
        position.company = unknown_company
        
        if commit:
            position.save()
        return position


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'document_type', 'file', 'description', 'is_default']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Document name'}),
            'document_type': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Brief description...'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        document = super().save(commit=False)
        if self.user:
            document.user = self.user
        if commit:
            document.save()
        return document


class JobApplicationWithInlineCompanyForm(forms.ModelForm):
    """Extended job application form with inline company creation"""
    
    # Inline company fields
    company_name = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
        label='Company Name'
    )
    company_website = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com'}),
        label='Company Website'
    )
    company_location = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, Country'}),
        label='Company Location'
    )
    company_industry = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Technology, Finance, etc.'}),
        label='Industry'
    )
    company_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Brief description about the company...'}),
        label='Company Description'
    )
    
    # Job position fields
    job_title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
        label='Job Title'
    )
    job_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Job description...'}),
        label='Job Description'
    )
    job_requirements = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Job requirements...'}),
        label='Job Requirements'
    )
    employment_type = forms.ChoiceField(
        choices=JobPosition.EMPLOYMENT_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Employment Type'
    )
    job_location = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job location'}),
        label='Job Location'
    )
    remote_allowed = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Remote Work Allowed'
    )
    job_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Job posting URL'}),
        label='Job Posting URL'
    )
    salary_min = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minimum salary'}),
        label='Minimum Salary'
    )
    salary_max = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Maximum salary'}),
        label='Maximum Salary'
    )

    class Meta:
        model = JobApplication
        fields = ['sender_email', 'status', 'priority', 'hr_email', 'hr_name', 'hr_phone',
                 'recruiter_email', 'recruiter_name', 'applied_date', 'deadline',
                 'resume', 'cover_letter', 'notes', 'salary_expectation']
        widgets = {
            'sender_email': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'hr_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'hr@company.com'}),
            'hr_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'HR Contact Name'}),
            'hr_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 123-4567'}),
            'recruiter_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'recruiter@company.com'}),
            'recruiter_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Recruiter Name'}),
            'applied_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'resume': forms.Select(attrs={'class': 'form-control'}),
            'cover_letter': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Additional notes...'}),
            'salary_expectation': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Expected salary'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            # Filter user emails
            user_emails = UserEmail.objects.filter(user=self.user, is_active=True)
            self.fields['sender_email'].queryset = user_emails
            
            # Set primary email as initial if exists
            primary_email = user_emails.filter(is_primary=True).first()
            if primary_email:
                self.fields['sender_email'].initial = primary_email
            elif user_emails.exists():
                # If no primary email, set first active email as initial
                self.fields['sender_email'].initial = user_emails.first()
            
            # Filter documents by user and document type
            self.fields['resume'].queryset = Document.objects.filter(
                user=self.user, document_type='RESUME'
            ).order_by('-is_default', '-created_at')
            self.fields['cover_letter'].queryset = Document.objects.filter(
                user=self.user, document_type='COVER_LETTER'
            ).order_by('-is_default', '-created_at')
            
            # Set default resume and cover letter if they exist
            default_resume = Document.objects.filter(
                user=self.user, document_type='RESUME', is_default=True
            ).first()
            if default_resume:
                self.fields['resume'].initial = default_resume
                
            default_cover_letter = Document.objects.filter(
                user=self.user, document_type='COVER_LETTER', is_default=True
            ).first()
            if default_cover_letter:
                self.fields['cover_letter'].initial = default_cover_letter

        # Add empty option to document and email fields
        self.fields['sender_email'].empty_label = "Select an email"
        self.fields['resume'].empty_label = "Select a resume"
        self.fields['cover_letter'].empty_label = "Select a cover letter"

    def clean(self):
        cleaned_data = super().clean()
        company_name = cleaned_data.get('company_name')
        job_title = cleaned_data.get('job_title')
        
        # Company name is always required for this form
        if not company_name:
            raise forms.ValidationError("Company name is required.")
        
        if not job_title:
            raise forms.ValidationError("Job title is required.")
            
        return cleaned_data

    def save(self, commit=True):
        application = super().save(commit=False)
        if self.user:
            application.user = self.user
        
        # Always create company - this form is specifically for creating applications with new companies
        company = Company.objects.create(
            name=self.cleaned_data['company_name'],
            website=self.cleaned_data.get('company_website', ''),
            location=self.cleaned_data.get('company_location', ''),
            industry=self.cleaned_data.get('company_industry', ''),
            description=self.cleaned_data.get('company_description', '')
        )
        
        # Create job position
        position = JobPosition.objects.create(
            company=company,  # Always the newly created company
            title=self.cleaned_data['job_title'],
            description=self.cleaned_data.get('job_description', ''),
            requirements=self.cleaned_data.get('job_requirements', ''),
            employment_type=self.cleaned_data.get('employment_type', 'FULL_TIME'),
            salary_min=self.cleaned_data.get('salary_min'),
            salary_max=self.cleaned_data.get('salary_max'),
            location=self.cleaned_data.get('job_location', ''),
            remote_allowed=self.cleaned_data.get('remote_allowed', False),
            job_url=self.cleaned_data.get('job_url', '')
        )
        
        application.position = position
        
        if commit:
            application.save()
        
        return application


class InterviewRoundForm(forms.ModelForm):
    class Meta:
        model = InterviewRound
        fields = ['round_number', 'interview_type', 'interviewer_name', 'interviewer_email',
                 'scheduled_date', 'duration_minutes', 'location', 'status', 'feedback', 'notes']
        widgets = {
            'round_number': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'interview_type': forms.Select(attrs={'class': 'form-control'}),
            'interviewer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Interviewer Name'}),
            'interviewer_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'interviewer@company.com'}),
            'scheduled_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duration in minutes'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location or meeting link'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Interview feedback...'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional notes...'}),
        }


class ApplicationNoteForm(forms.ModelForm):
    class Meta:
        model = ApplicationNote
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add a note about this application...'}),
        }


class EmailApplicationForm(forms.Form):
    """Form for sending application emails to HR"""
    to_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'hr@company.com'}),
        label='To Email'
    )
    cc_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'recruiter@company.com'}),
        label='CC Email (Optional)'
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Application for [Position] - [Your Name]'}),
        label='Subject'
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Dear Hiring Manager,\n\nI am writing to express my interest...'}),
        label='Message'
    )
    attach_resume = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Attach Resume'
    )
    attach_cover_letter = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Attach Cover Letter'
    )

    def __init__(self, *args, **kwargs):
        application = kwargs.pop('application', None)
        super().__init__(*args, **kwargs)
        
        if application:
            # Pre-populate fields based on application
            self.fields['to_email'].initial = application.hr_email or application.recruiter_email
            self.fields['cc_email'].initial = application.recruiter_email if application.hr_email else None
            self.fields['subject'].initial = f"Application for {application.position.title} - {application.user.get_full_name() or application.user.username}"
            
            # Create a default message
            company_name = application.position.company.name
            position_title = application.position.title
            user_name = application.user.get_full_name() or application.user.username
            
            default_message = f"""Dear Hiring Manager,

I am writing to express my strong interest in the {position_title} position at {company_name}. I have attached my resume and cover letter for your review.

I am excited about the opportunity to contribute to your team and would welcome the chance to discuss how my skills and experience align with your needs.

Thank you for your time and consideration. I look forward to hearing from you.

Best regards,
{user_name}"""
            
            self.fields['message'].initial = default_message


class HREmailForm(forms.Form):
    """Enhanced form for sending professional emails to HR with templates"""
    sender_email = forms.ModelChoiceField(
        queryset=UserEmail.objects.none(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Send From Email',
        help_text='Select which email address to send from'
    )
    hr_name = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'HR Manager Name (Optional)'}),
        label='HR Contact Name',
        help_text='For personalized greeting (e.g., "Dear John Smith")'
    )
    to_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'hr@company.com'}),
        label='HR Email Address'
    )
    cc_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'recruiter@company.com (Optional)'}),
        label='CC Email',
        help_text='Optional - for copying recruiters or other contacts'
    )
    custom_message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': 6, 
            'placeholder': 'Add a personalized message about why you\'re interested in this role and what makes you a great fit...'
        }),
        label='Personal Message',
        help_text='Optional - This will replace the default message in the email template'
    )
    attach_resume = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Attach Resume'
    )
    attach_cover_letter = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Attach Cover Letter'
    )
    use_template = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Use Professional Email Template',
        help_text='Recommended - Uses an attractive HTML email template'
    )

    def __init__(self, *args, **kwargs):
        application = kwargs.pop('application', None)
        super().__init__(*args, **kwargs)
        
        if application:
            # Set up sender email choices
            user_emails = UserEmail.objects.filter(user=application.user)
            self.fields['sender_email'].queryset = user_emails
            
            # Set primary email as initial
            primary_email = user_emails.filter(is_primary=True).first()
            if primary_email:
                self.fields['sender_email'].initial = primary_email
            elif user_emails.exists():
                self.fields['sender_email'].initial = user_emails.first()
                
            # Pre-populate fields based on application
            self.fields['to_email'].initial = application.hr_email or application.recruiter_email
            self.fields['cc_email'].initial = application.recruiter_email if application.hr_email else None
            self.fields['hr_name'].initial = application.hr_name
            
            # Check if documents are available
            if not application.resume:
                self.fields['attach_resume'].initial = False
                self.fields['attach_resume'].widget.attrs['disabled'] = True
                self.fields['attach_resume'].help_text = 'No resume uploaded for this application'
            
            if not application.cover_letter:
                self.fields['attach_cover_letter'].initial = False
                self.fields['attach_cover_letter'].widget.attrs['disabled'] = True
                self.fields['attach_cover_letter'].help_text = 'No cover letter uploaded for this application'

    def clean(self):
        cleaned_data = super().clean()
        attach_resume = cleaned_data.get('attach_resume')
        attach_cover_letter = cleaned_data.get('attach_cover_letter')
        
        if not attach_resume and not attach_cover_letter:
            raise forms.ValidationError(
                'You must attach at least one document (resume or cover letter) to send the email.'
            )
        
        return cleaned_data