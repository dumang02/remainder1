from django.db import models

# Create your models here.
# myapp/models.py
from django.db import models

MEDICINE_TYPE_CHOICES = [
    ('tablet', 'Tablet'),
    ('capsule', 'Capsule'),
    ('syrup', 'Syrup'),
    ('injection', 'Injection'),
    # Add more as needed
]

class MedicineData(models.Model):
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=50)
    medicine_type = models.CharField(max_length=50, choices=MEDICINE_TYPE_CHOICES)
    reminder_duration = models.PositiveIntegerField()  # in days
    photo = models.ImageField(upload_to='photos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

    @property
    def expiry_date(self):
        from datetime import timedelta
        return self.created_at + timedelta(days=self.reminder_duration)


# myapp/models.py
from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError

def validate_password_match(value):
    # Used in form, not model
    pass

class regsiter(models.Model):
    A_id = models.AutoField(primary_key=True, auto_created=True)
    
    username = models.CharField(
        max_length=20,
        validators=[MinLengthValidator(3, "Username must be at least 3 characters")]
    )

    email = models.EmailField(unique=True)

    password = models.CharField(
        max_length=128,  # Store hashed password
        validators=[
            MinLengthValidator(8, "Password must be at least 8 characters"),
            RegexValidator(
                regex=r'^(?=.*[A-Za-z])(?=.*\d).+$',
                message="Password must contain letters and numbers"
            )
        ]
    )

    def __str__(self):
        return self.email
