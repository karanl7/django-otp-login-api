from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone

class User(models.Model):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)

