"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views
from django.http import HttpResponse
from reportlab.pdfgen import canvas

urlpatterns = [
   path('dashboard',views.dashboard,name='dashboard'),
   path('all_patients',views.all_patients,name='setall_patientst'),
   path('before_reminders',views.before_reminders,name='before_reminders'),
   path('settings',views.settings,name='setting'),
   path('medicine-form/', views.medicine_form_page, name='medicine_form'),  
   path('', views.login_view, name='login'),
   path('logout/', views.logout_view, name='logout'),
    path('before-reminders/', views.before_reminder_view, name='before_reminder'),
    path('before-reminders/pdf/', views.download_before_pdf, name='download_before_pdf'),
    path('before-reminders/excel/', views.download_before_excel, name='download_before_excel'),
    path('one-day-reminders/', views.one_day_reminder_view, name='one_day_reminder'),
path('one-day-reminders/pdf/', views.download_one_day_pdf, name='download_one_day_pdf'),
path('one-day-reminders/excel/', views.download_one_day_excel, name='download_one_day_excel'),

]

def download_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reminder.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 750, "Hello, this is your reminder PDF!")
    p.showPage()
    p.save()
    return response
