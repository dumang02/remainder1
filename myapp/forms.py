from django import forms
from .models import MedicineData, regsiter
import re

DURATION_CHOICES = [
    (2, "2 Days"),
    (5, "5 Days"),
    (10, "10 Days"),
    (15, "15 Days"),
    (30, "1 Month"),
    (90, "3 Months"),
    (180, "6 Months"),
]

MEDICINE_TYPE_CHOICES = [
    ('SELECT MEDICINE','SELECT MEDICINE '),
    ('tablet', 'Tablet'),
    ('capsule', 'Capsule'),
    ('syrup', 'Syrup'),
    ('injection', 'Injection'),
    # Add more as needed
]

class MedicineForm(forms.ModelForm):
    reminder_duration = forms.ChoiceField(
        choices=DURATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Reminder Duration"
    )
    medicine_type = forms.ChoiceField(
        choices=MEDICINE_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Medicine Type"
    )

    class Meta:
        model = MedicineData
        fields = '__all__'
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_full_name(self):
        name = self.cleaned_data.get('full_name')
        if not re.match(r'^[A-Za-z ]+$', name):
            raise forms.ValidationError("Only letters and spaces allowed.")
        return name

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not re.match(r'^[0-9]{10}$', phone):
            raise forms.ValidationError("Enter a valid 10-digit phone number.")
        return phone

    def clean_reminder_duration(self):
        return int(self.cleaned_data['reminder_duration'])

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if not photo:
            raise forms.ValidationError("Photo is required.")
        if photo.size > 2 * 1024 * 1024:
            raise forms.ValidationError("Photo must be under 2MB.")
        return photo

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control text'}))
    class Meta:
        model = regsiter
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control text'}),
            'email': forms.EmailInput(attrs={'class': 'form-control text'}),
        }

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control text'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control text'}))



