from django.db import models
from django.utils import timezone
from datetime import timedelta
from adminside.models import Staff

class PasswordResetOTP(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(seconds=120)

    def __str__(self):
        return f"{self.staff.staff_username} - {self.otp}"
