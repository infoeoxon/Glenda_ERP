from django.db import models

from register_app.models import CustomUser


# Create your models here.
class customer_registration(models.Model):
    is_distributor = models.BooleanField(default=False)  # Admin status
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    pincode = models.CharField(max_length=6, null=True)
    state = models.CharField(max_length=200, null=True)
    district = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    GST_CHOICES = [('yes', 'Yes'), ('no', 'No')]
    GST_yes_or_no = models.CharField(max_length=15, choices=GST_CHOICES, default='yes', null=True)
    GST_number = models.CharField(max_length=15, null=True, blank=True)
    PAN_CHOICES = [('yes', 'Yes'), ('no', 'No')]
    pan_yes_or_no = models.CharField(max_length=10, choices=PAN_CHOICES, default='yes', null=True)
    PAN_number = models.CharField(max_length=10, null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.name
