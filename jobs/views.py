from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta

from .models import Company, JobPosition, JobApplication, Document, InterviewRound, ApplicationNote, UserEmail
from .forms import (CompanyForm, JobPositionForm, JobApplicationForm, DocumentForm, 
                   InterviewRoundForm, ApplicationNoteForm, EmailApplicationForm, JobApplicationWithInlineCompanyForm, HREmailForm, UserEmailForm)
from .email_utils import send_application_email, send_hr_application_email


def home(request):
    """Home page with dashboard overview"""
    if request.user.is_authenticated:
        # Get user's application statistics
        total_applications = JobApplication.objects.filter(user=request.user).count()
        pending_applications = JobApplication.objects.filter(
            user=request.user, 
            status__in=['DRAFT', 'APPLIED']
        ).count()
        interview_applications = JobApplication.objects.filter(
            user=request.user,
            status__in=['PHONE_SCREEN', 'TECHNICAL_INTERVIEW', 'ONSITE_INTERVIEW', 'FINAL_INTERVIEW']
        ).count()
        
        # Recent applications
        recent_applications = JobApplication.objects.filter(
            user=request.user
        ).order_by('-created_at')[:5]
        
        # Upcoming interviews
        upcoming_interviews = InterviewRound.objects.filter(
            application__user=request.user,
            scheduled_date__gte=timezone.now(),
            status='SCHEDULED'
        ).order_by('scheduled_date')[:5]
        
        context = {
            'total_applications': total_applications,
            'pending_applications': pending_applications,
            'interview_applications': interview_applications,
            'recent_applications': recent_applications,
            'upcoming_interviews': upcoming_interviews,
        }
        return render(request, 'jobs/dashboard.html', context)
    else:
        return render(request, 'jobs/home.html')


@login_required
def application_list(request):
    """List all job applications for the current user"""
    applications = JobApplication.objects.filter(user=request.user)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        applications = applications.filter(
            Q(position__title__icontains=search_query) |
            Q(position__company__name__icontains=search_query) |
            Q(notes__icontains=search_query)
        )
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    # Filter by priority
    priority_filter = request.GET.get('priority')
    if priority_filter:
        applications = applications.filter(priority=priority_filter)
    
    # Order by creation date (newest first)
    applications = applications.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(applications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter choices for the template
    status_choices = JobApplication.STATUS_CHOICES
    priority_choices = JobApplication.PRIORITY_CHOICES
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'status_choices': status_choices,
        'priority_choices': priority_choices,
    }
    return render(request, 'jobs/application_list.html', context)


@login_required
def application_detail(request, pk):
    """View details of a specific job application"""
    application = get_object_or_404(JobApplication, pk=pk, user=request.user)
    interview_rounds = application.interview_rounds.all().order_by('round_number')
    notes = application.application_notes.all().order_by('-created_at')
    
    context = {
        'application': application,
        'interview_rounds': interview_rounds,
        'notes': notes,
    }
    return render(request, 'jobs/application_detail.html', context)


@login_required
def application_create(request):
    """Create a new job application"""
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, user=request.user)
        if form.is_valid():
            application = form.save()
            messages.success(request, 'Job application created successfully!')
            return redirect('jobs:application_detail', pk=application.pk)
    else:
        form = JobApplicationForm(user=request.user)
    
    context = {'form': form, 'title': 'Create New Application'}
    return render(request, 'jobs/application_form.html', context)


@login_required
def application_create_with_company(request):
    """Create a new job application with inline company creation"""
    if request.method == 'POST':
        form = JobApplicationWithInlineCompanyForm(request.POST, user=request.user)
        if form.is_valid():
            application = form.save()
            messages.success(request, 'Job application and company created successfully!')
            return redirect('jobs:application_detail', pk=application.pk)
    else:
        form = JobApplicationWithInlineCompanyForm(user=request.user)
    
    context = {'form': form, 'title': 'Create New Application with Company'}
    return render(request, 'jobs/application_form_with_company.html', context)


@login_required
def application_edit(request, pk):
    """Edit an existing job application"""
    application = get_object_or_404(JobApplication, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, instance=application, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job application updated successfully!')
            return redirect('jobs:application_detail', pk=application.pk)
    else:
        form = JobApplicationForm(instance=application, user=request.user)
    
    context = {'form': form, 'application': application, 'title': 'Edit Application'}
    return render(request, 'jobs/application_form.html', context)


@login_required
def application_delete(request, pk):
    """Delete a job application"""
    application = get_object_or_404(JobApplication, pk=pk, user=request.user)
    
    if request.method == 'POST':
        application.delete()
        messages.success(request, 'Job application deleted successfully!')
        return redirect('jobs:application_list')
    
    context = {'application': application}
    return render(request, 'jobs/application_confirm_delete.html', context)


@login_required
def send_application_email_view(request, pk):
    """Send application email to HR"""
    application = get_object_or_404(JobApplication, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = EmailApplicationForm(request.POST, application=application)
        if form.is_valid():
            success = send_application_email(
                application=application,
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
                to_email=form.cleaned_data['to_email'],
                cc_email=form.cleaned_data['cc_email'],
                attach_resume=form.cleaned_data['attach_resume'],
                attach_cover_letter=form.cleaned_data['attach_cover_letter']
            )
            
            if success:
                messages.success(request, 'Application email sent successfully!')
                return redirect('jobs:application_detail', pk=application.pk)
            else:
                messages.error(request, 'Failed to send email. Please check your email settings.')
    else:
        form = EmailApplicationForm(application=application)
    
    context = {
        'form': form,
        'application': application,
        'title': 'Send Application Email'
    }
    return render(request, 'jobs/send_email.html', context)


@login_required
def send_hr_email_view(request, pk):
    """Send professional application email to HR with attractive template"""
    application = get_object_or_404(JobApplication, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = HREmailForm(request.POST, application=application)
        if form.is_valid():
            # Save the sender email and HR details to the application
            application.sender_email = form.cleaned_data['sender_email']
            application.hr_email = form.cleaned_data['to_email']
            application.hr_name = form.cleaned_data['hr_name']
            application.save()
            
            success = send_hr_application_email(
                application=application,
                sender_email=form.cleaned_data['sender_email'],
                to_email=form.cleaned_data['to_email'],
                cc_email=form.cleaned_data['cc_email'],
                custom_message=form.cleaned_data['custom_message'],
                hr_name=form.cleaned_data['hr_name'],
                attach_resume=form.cleaned_data['attach_resume'],
                attach_cover_letter=form.cleaned_data['attach_cover_letter']
            )
            
            if success:
                application.mark_as_sent()
                messages.success(request, 'Professional application email sent successfully to HR!')
                return redirect('jobs:application_detail', pk=application.pk)
            else:
                messages.error(request, 'Failed to send email. Please check your email settings and try again.')
    else:
        form = HREmailForm(application=application)
    
    context = {
        'form': form,
        'application': application,
        'title': 'Send Professional Email to HR',
        'show_preview': True  # Enable email preview feature
    }
    return render(request, 'jobs/send_hr_email.html', context)


@login_required
def document_list(request):
    """List all documents for the current user"""
    documents = Document.objects.filter(user=request.user).order_by('-created_at')
    
    # Filter by document type
    doc_type_filter = request.GET.get('type')
    if doc_type_filter:
        documents = documents.filter(document_type=doc_type_filter)
    
    # Pagination
    paginator = Paginator(documents, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    document_types = Document.DOCUMENT_TYPE_CHOICES
    
    context = {
        'page_obj': page_obj,
        'doc_type_filter': doc_type_filter,
        'document_types': document_types,
    }
    return render(request, 'jobs/document_list.html', context)


@login_required
def document_upload(request):
    """Upload a new document"""
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            document = form.save()
            messages.success(request, 'Document uploaded successfully!')
            return redirect('jobs:document_list')
    else:
        form = DocumentForm(user=request.user)
    
    context = {'form': form, 'title': 'Upload Document'}
    return render(request, 'jobs/document_form.html', context)


@login_required
def document_delete(request, pk):
    """Delete a document"""
    document = get_object_or_404(Document, pk=pk, user=request.user)
    
    if request.method == 'POST':
        document.delete()
        messages.success(request, 'Document deleted successfully!')
        return redirect('jobs:document_list')
    
    context = {'document': document}
    return render(request, 'jobs/document_confirm_delete.html', context)


@login_required
def company_list(request):
    """List all companies"""
    companies = Company.objects.all().order_by('name')
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        companies = companies.filter(
            Q(name__icontains=search_query) |
            Q(industry__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(companies, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'jobs/company_list.html', context)


@login_required
def company_create(request):
    """Create a new company"""
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save()
            messages.success(request, 'Company created successfully!')
            return redirect('jobs:company_list')
    else:
        form = CompanyForm()
    
    context = {'form': form, 'title': 'Add New Company'}
    return render(request, 'jobs/company_form.html', context)


@login_required
def company_edit(request, pk):
    """Edit an existing company"""
    company = get_object_or_404(Company, pk=pk)
    
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company updated successfully!')
            return redirect('jobs:company_list')
    else:
        form = CompanyForm(instance=company)
    
    context = {'form': form, 'company': company, 'title': 'Edit Company'}
    return render(request, 'jobs/company_form.html', context)


@login_required
def company_delete(request, pk):
    """Delete a company"""
    company = get_object_or_404(Company, pk=pk)
    
    if request.method == 'POST':
        company_name = company.name
        company.delete()
        messages.success(request, f'Company "{company_name}" deleted successfully!')
        return redirect('jobs:company_list')
    
    context = {'company': company, 'title': 'Delete Company'}
    return render(request, 'jobs/company_confirm_delete.html', context)


@login_required
def position_create(request):
    """Create a new job position"""
    if request.method == 'POST':
        form = JobPositionForm(request.POST)
        if form.is_valid():
            position = form.save()
            messages.success(request, 'Job position created successfully!')
            # Redirect to create application for this position
            return redirect('jobs:application_create') + f'?position={position.pk}'
    else:
        form = JobPositionForm()
    
    context = {'form': form, 'title': 'Add New Job Position'}
    return render(request, 'jobs/position_form.html', context)


@login_required
def add_interview_round(request, application_pk):
    """Add an interview round to an application"""
    application = get_object_or_404(JobApplication, pk=application_pk, user=request.user)
    
    if request.method == 'POST':
        form = InterviewRoundForm(request.POST)
        if form.is_valid():
            interview_round = form.save(commit=False)
            interview_round.application = application
            interview_round.save()
            messages.success(request, 'Interview round added successfully!')
            return redirect('jobs:application_detail', pk=application.pk)
    else:
        # Set default round number
        last_round = application.interview_rounds.order_by('-round_number').first()
        initial_round = (last_round.round_number + 1) if last_round else 1
        form = InterviewRoundForm(initial={'round_number': initial_round})
    
    context = {
        'form': form,
        'application': application,
        'title': 'Add Interview Round'
    }
    return render(request, 'jobs/interview_round_form.html', context)


@login_required
def add_application_note(request, application_pk):
    """Add a note to an application"""
    application = get_object_or_404(JobApplication, pk=application_pk, user=request.user)
    
    if request.method == 'POST':
        form = ApplicationNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.application = application
            note.save()
            messages.success(request, 'Note added successfully!')
            return redirect('jobs:application_detail', pk=application.pk)
    else:
        form = ApplicationNoteForm()
    
    context = {
        'form': form,
        'application': application,
        'title': 'Add Note'
    }
    return render(request, 'jobs/note_form.html', context)


@login_required
def statistics(request):
    """Show application statistics"""
    user_applications = JobApplication.objects.filter(user=request.user)
    total_applications = user_applications.count()
    
    # Status statistics with percentages
    status_stats = []
    for status_code, status_name in JobApplication.STATUS_CHOICES:
        status_count = user_applications.filter(status=status_code).count()
        percentage = round((status_count / total_applications * 100) if total_applications > 0 else 0, 1)
        status_stats.append((status_code, status_count, percentage))
    
    # Calculate derived metrics
    applications_this_month = user_applications.filter(
        created_at__month=timezone.now().month,
        created_at__year=timezone.now().year
    ).count()
    
    interview_count = user_applications.filter(
        status__in=['PHONE_SCREEN', 'TECHNICAL_INTERVIEW', 'ONSITE_INTERVIEW', 'FINAL_INTERVIEW']
    ).count()
    
    response_rate = round((interview_count / total_applications * 100) if total_applications > 0 else 0, 1)
    interview_rate = round((interview_count / total_applications * 100) if total_applications > 0 else 0, 1)
    offer_count = user_applications.filter(status='OFFER').count()
    offer_rate = round((offer_count / total_applications * 100) if total_applications > 0 else 0, 1)
    rejection_count = user_applications.filter(status='REJECTED').count()
    rejection_rate = round((rejection_count / total_applications * 100) if total_applications > 0 else 0, 1)
    
    # Top industries
    top_industries = user_applications.values('position__company__industry').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # Top companies
    top_companies = user_applications.values('position__company__name', 'position__company').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # Timeline data (last 6 months)
    from datetime import datetime, timedelta
    from django.db.models.functions import TruncMonth
    
    six_months_ago = timezone.now() - timedelta(days=180)
    monthly_stats = user_applications.filter(
        created_at__gte=six_months_ago
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    # Format timeline data
    timeline_data = []
    max_count = max([m['count'] for m in monthly_stats]) if monthly_stats else 1
    for stat in monthly_stats:
        timeline_data.append({
            'month': stat['month'].strftime('%b'),
            'count': stat['count'],
            'percentage': round((stat['count'] / max_count * 100) if max_count > 0 else 0, 1)
        })
    
    # Recent applications
    recent_applications = user_applications.order_by('-created_at')[:6]
    
    context = {
        'status_stats': status_stats,
        'total_applications': total_applications,
        'applications_this_month': applications_this_month,
        'interview_count': interview_count,
        'response_rate': response_rate,
        'interview_rate': interview_rate,
        'offer_rate': offer_rate,
        'rejection_rate': rejection_rate,
        'top_industries': [(item['position__company__industry'] or 'Not Specified', item['count']) for item in top_industries],
        'top_companies': [(Company.objects.get(pk=item['position__company']), item['count']) for item in top_companies if item['position__company']],
        'timeline_data': timeline_data,
        'recent_applications': recent_applications,
    }
    return render(request, 'jobs/statistics.html', context)


@login_required
def user_email_list(request):
    """List all user emails"""
    user_emails = UserEmail.objects.filter(user=request.user).order_by('-is_primary', 'email_type', 'email')
    return render(request, 'jobs/user_email_list.html', {'user_emails': user_emails})


@login_required
def user_email_create(request):
    """Create a new user email"""
    if request.method == 'POST':
        form = UserEmailForm(request.POST, user=request.user)
        if form.is_valid():
            user_email = form.save(commit=False)
            user_email.user = request.user
            user_email.save()
            messages.success(request, 'Email address added successfully!')
            return redirect('jobs:user_email_list')
    else:
        form = UserEmailForm(user=request.user)
    
    return render(request, 'jobs/user_email_form.html', {'form': form, 'title': 'Add New Email'})


@login_required
def user_email_edit(request, pk):
    """Edit a user email"""
    user_email = get_object_or_404(UserEmail, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = UserEmailForm(request.POST, instance=user_email, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Email address updated successfully!')
            return redirect('jobs:user_email_list')
    else:
        form = UserEmailForm(instance=user_email, user=request.user)
    
    return render(request, 'jobs/user_email_form.html', {'form': form, 'title': 'Edit Email'})


@login_required
def user_email_delete(request, pk):
    """Delete a user email"""
    user_email = get_object_or_404(UserEmail, pk=pk, user=request.user)
    
    if request.method == 'POST':
        email_address = user_email.email
        user_email.delete()
        messages.success(request, f'Email address {email_address} deleted successfully!')
        return redirect('jobs:user_email_list')
    
    return render(request, 'jobs/user_email_confirm_delete.html', {'user_email': user_email})


@login_required
def user_email_set_default(request, pk):
    """Set an email as primary"""
    user_email = get_object_or_404(UserEmail, pk=pk, user=request.user)
    user_email.is_primary = True
    user_email.save()  # This will automatically unset other primary emails due to model logic
    messages.success(request, f'Set {user_email.email} as primary email!')
    return redirect('jobs:user_email_list')
