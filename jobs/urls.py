from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    # Home and dashboard
    path('', views.home, name='home'),
    
    # Job Applications
    path('applications/', views.application_list, name='application_list'),
    path('applications/create/', views.application_create, name='application_create'),
    path('applications/create-with-company/', views.application_create_with_company, name='application_create_with_company'),
    path('applications/<int:pk>/', views.application_detail, name='application_detail'),
    path('applications/<int:pk>/edit/', views.application_edit, name='application_edit'),
    path('applications/<int:pk>/delete/', views.application_delete, name='application_delete'),
    path('applications/<int:pk>/send-email/', views.send_application_email_view, name='send_application_email'),
    path('applications/<int:pk>/send-hr-email/', views.send_hr_email_view, name='send_hr_email'),
    
    # Interview Rounds
    path('applications/<int:application_pk>/add-interview/', views.add_interview_round, name='add_interview_round'),
    
    # Application Notes
    path('applications/<int:application_pk>/add-note/', views.add_application_note, name='add_application_note'),
    
    # Documents
    path('documents/', views.document_list, name='document_list'),
    path('documents/upload/', views.document_upload, name='document_upload'),
    path('documents/<int:pk>/edit/', views.document_edit, name='document_edit'),
    path('documents/<int:pk>/delete/', views.document_delete, name='document_delete'),
    
    # Companies
    path('companies/', views.company_list, name='company_list'),
    path('companies/create/', views.company_create, name='company_create'),
    path('companies/add/', views.company_create, name='company_add'),  # Alias for create
    path('companies/<int:pk>/edit/', views.company_edit, name='company_edit'),
    path('companies/<int:pk>/delete/', views.company_delete, name='company_delete'),
    
    # Job Positions
    path('positions/create/', views.position_create, name='position_create'),
    
    # Statistics
    path('statistics/', views.statistics, name='statistics'),
    
    # User Email Management
    path('emails/', views.user_email_list, name='user_email_list'),
    path('emails/add/', views.user_email_create, name='user_email_create'),
    path('emails/<int:pk>/edit/', views.user_email_edit, name='user_email_edit'),
    path('emails/<int:pk>/delete/', views.user_email_delete, name='user_email_delete'),
    path('emails/<int:pk>/set-default/', views.user_email_set_default, name='user_email_set_default'),
]