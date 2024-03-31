from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    pass

class AdditionalInfo(models.Model):
    full_name = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='additional_info')
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
  

    def __str__(self):
        return self.user.full_name




