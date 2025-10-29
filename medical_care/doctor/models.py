from django.db import models
from core.models import CustomUser

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="doctor")
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)

    department = models.CharField(max_length=100)

    # ✅ Extra recommended fields
    license_number = models.CharField(max_length=50, unique=True)  # Medical license ID
    qualification = models.CharField(max_length=200)  # e.g. MBBS, MD, MS
    years_of_experience = models.PositiveIntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    is_verified = models.BooleanField(default=False)  # Admin approval required
    document=models.ImageField(upload_to="documents",null= True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} ({self.specialization})"

