from django.db import models

from inventory_app.models import Add_RawMaterial
from purchase_app.models import RawMaterials, RFQ_raw_materials
from register_app.models import CustomUser


# Create your models here.
class vendor_request(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    upload_file = models.ImageField(upload_to='images/', null=True)
    remarks=models.CharField(max_length=150,null=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')





class vendor_register(models.Model):
    is_vendor = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    company_name = models.CharField(max_length=200, null=True)
    vendor_district = models.CharField(max_length=150, null=True)
    vendor_state = models.CharField(max_length=200, null=True)
    vendor_country = models.CharField(max_length=150, null=True)
    vendor_pincode = models.IntegerField(null=True)
    PAN_CHOICES = [('yes', 'Yes'), ('no', 'No')]
    pan_yes_or_no = models.CharField(max_length=10, choices=PAN_CHOICES, default='yes', null=True)
    vendor_PANNBR = models.CharField(max_length=150, null=True, blank=True)
    vendor_Street = models.CharField(max_length=200, null=True)
    vendor_Landmark = models.CharField(max_length=200, null=True)
    vendor_Building = models.CharField(max_length=200, null=True)
    materials_name = models.ManyToManyField(Add_RawMaterial, blank=True)
    status = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.company_name or "Vendor"


class vendor_quotation(models.Model):
    vendor=models.ForeignKey(vendor_register, on_delete=models.CASCADE, null=True)
    quotation = models.ForeignKey(RFQ_raw_materials, on_delete=models.CASCADE, null=True)
    unit_Price=models.CharField(max_length=150, null=True)
    total_Price=models.IntegerField( null=True)
    discount=models.CharField(max_length=150, null=True)
    payment_terms=models.CharField(max_length=150, null=True)
    document=models.ImageField(upload_to='images/', null=True)
    time_frame=models.CharField(max_length=150, null=True)
    special_notes=models.CharField(max_length=150, null=True)
    status=models.CharField(max_length=150, null=True)