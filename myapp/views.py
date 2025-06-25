from django.shortcuts import render, redirect
from .models import *
# Create your views here.


from django.shortcuts import render, redirect
from .forms import MedicineForm, RegisterForm, LoginForm
from django.contrib import messages

def medicine_form_page(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = MedicineForm()
    return render(request, 'myapp/form.html', {'form': form})



def dashboard(request):
    return render(request, 'myapp/dashboard.html')


def all_patients(request):
    patients = MedicineData.objects.all()
    return render(request, 'myapp/all_patients.html', {'patients': patients})

def before_reminders(request):
    return render(request, 'myapp/before_reminders.html')


def settings(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # or your desired success page
    else:
        form = RegisterForm()
    return render(request, 'myapp/settings.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = regsiter.objects.get(email=email, password=password)
                request.session['user_email'] = user.email
                return redirect('dashboard')
            except regsiter.DoesNotExist:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    return render(request, 'myapp/login.html', {'form': form})

def logout_view(request):
    try:
        del request.session['user_email']
    except KeyError:
        pass
    return redirect('login')


# myapp/views.py
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import MedicineData
from django.template.loader import get_template
from xhtml2pdf import pisa
import openpyxl
from django.http import HttpResponse

# Get 2–3 days before expiry
def get_reminder_queryset():
    today = timezone.now().date()
    reminders = []

    for obj in MedicineData.objects.all():
        expiry = obj.expiry_date.date()
        days_left = (expiry - today).days
        if 2 <= days_left <= 3:
            reminders.append(obj)
    return reminders

# Render Before Reminder Page
def before_reminder_view(request):
    reminders = get_reminder_queryset()
    return render(request, 'myapp/before_reminder.html', {'reminders': reminders})

# PDF download for before reminders
def download_before_pdf(request):
    reminders = get_reminder_queryset()
    template_path = 'myapp/reminder_pdf_template.html'
    context = {'reminders': reminders}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="before_reminder.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa.CreatePDF(html, dest=response)
    return response

# Excel download for before reminders
def download_before_excel(request):
    reminders = get_reminder_queryset()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Reminders"
    ws.append(['Full Name', 'Phone', 'City', 'Medicine Type', 'Expiry Date'])

    for user in reminders:
        ws.append([
            user.full_name,
            user.phone_number,
            user.city,
            user.medicine_type,
            user.expiry_date.strftime("%Y-%m-%d"),
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="before_reminder.xlsx"'
    wb.save(response)
    return response


# Filter for 1-day before expiry
def get_one_day_reminders():
    today = timezone.now().date()
    reminders = []

    for obj in MedicineData.objects.all():
        expiry = obj.expiry_date.date()
        days_left = (expiry - today).days
        if days_left == 1:
            reminders.append(obj)
    return reminders

# Show 1-day reminder page
def one_day_reminder_view(request):
    reminders = get_one_day_reminders()
    return render(request, 'myapp/before_reminder.html', {'reminders': reminders})

# Download 1-day reminders as PDF
def download_one_day_pdf(request):
    reminders = get_one_day_reminders()
    template_path = 'myapp/reminder_pdf_template.html'  # Reuse the same template
    context = {'reminders': reminders}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="1day_reminder.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa.CreatePDF(html, dest=response)
    return response

# Download 1-day reminders as Excel
def download_one_day_excel(request):
    reminders = get_one_day_reminders()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "1-Day Reminders"
    ws.append(['Full Name', 'Phone', 'City', 'Medicine Type', 'Expiry Date'])

    for user in reminders:
        ws.append([
            user.full_name,
            user.phone_number,
            user.city,
            user.medicine_type,
            user.expiry_date.strftime("%Y-%m-%d"),
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="1day_reminder.xlsx"'
    wb.save(response)
    return response



