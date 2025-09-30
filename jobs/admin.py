from django.contrib import admin
from .models import Company, JobPosition, Document, JobApplication, InterviewRound, ApplicationNote


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'industry', 'created_at']
    list_filter = ['industry', 'created_at']
    search_fields = ['name', 'location', 'industry']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(JobPosition)
class JobPositionAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'employment_type', 'location', 'remote_allowed', 'created_at']
    list_filter = ['employment_type', 'remote_allowed', 'company', 'created_at']
    search_fields = ['title', 'company__name', 'location']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['company']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'document_type', 'is_default', 'created_at']
    list_filter = ['document_type', 'is_default', 'created_at']
    search_fields = ['name', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['user']


class InterviewRoundInline(admin.TabularInline):
    model = InterviewRound
    extra = 0
    readonly_fields = ['created_at', 'updated_at']


class ApplicationNoteInline(admin.TabularInline):
    model = ApplicationNote
    extra = 0
    readonly_fields = ['created_at', 'updated_at']


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'position', 'status', 'priority', 'applied_date', 'email_sent', 'created_at']
    list_filter = ['status', 'priority', 'email_sent', 'applied_date', 'created_at', 'position__company']
    search_fields = ['user__username', 'position__title', 'position__company__name', 'hr_name', 'recruiter_name']
    readonly_fields = ['created_at', 'updated_at', 'email_sent_date']
    raw_id_fields = ['user', 'position', 'resume', 'cover_letter']
    inlines = [InterviewRoundInline, ApplicationNoteInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'position', 'status', 'priority')
        }),
        ('Contact Information', {
            'fields': ('hr_email', 'hr_name', 'recruiter_email', 'recruiter_name')
        }),
        ('Application Details', {
            'fields': ('applied_date', 'deadline', 'resume', 'cover_letter', 'salary_expectation')
        }),
        ('Email Status', {
            'fields': ('email_sent', 'email_sent_date')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(InterviewRound)
class InterviewRoundAdmin(admin.ModelAdmin):
    list_display = ['application', 'round_number', 'interview_type', 'scheduled_date', 'status', 'interviewer_name']
    list_filter = ['interview_type', 'status', 'scheduled_date', 'created_at']
    search_fields = ['application__user__username', 'application__position__title', 'interviewer_name', 'interviewer_email']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['application']


@admin.register(ApplicationNote)
class ApplicationNoteAdmin(admin.ModelAdmin):
    list_display = ['application', 'note_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['application__user__username', 'application__position__title', 'note']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['application']
    
    def note_preview(self, obj):
        return obj.note[:50] + '...' if len(obj.note) > 50 else obj.note
    note_preview.short_description = 'Note Preview'
