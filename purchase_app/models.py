from django.db import models



# Create your models here.
class RawMaterialCategory(models.Model):
    category_name = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.category_name


class RawMaterials(models.Model):
    category = models.ForeignKey(RawMaterialCategory, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=150, null=True, unique=True)
    size = models.CharField(max_length=150, null=True)
    color = models.CharField(max_length=150, null=True)
    image = models.ImageField(upload_to='images/', null=True)
    date = models.DateField(auto_now=True)
    total_stock = models.IntegerField(default=0)  # Field to track total stock

    def __str__(self):
        return self.name


# new code begins here

class RFQ_raw_materials(models.Model):
    rfq_number = models.CharField(max_length=50,null=True)
    request_date = models.DateField(auto_now_add=True)
    request_time = models.TimeField(auto_now_add=True)
    requested_by = models.CharField(max_length=220, null=True)
    approver = models.CharField(max_length=220, null=True)
    material_category = models.ForeignKey('inventory_app.AddCategory', on_delete=models.CASCADE, null=True, related_name='rfq_raw_material_category')
    material_name = models.ForeignKey('inventory_app.Add_RawMaterial', on_delete=models.CASCADE, null=True, related_name='rfq_raw_material_name')
    quantity_needed = models.IntegerField()
    batch_requirements = models.TextField(null=True, blank=True)
    quality_standards = models.FileField(upload_to='quality_standards/', null=True, blank=True)
    expected_delivery_date = models.DateField()
    vendor_list = models.ManyToManyField('vendor_app.vendor_register', related_name='vendor_list_rfq')  # Changed to ManyToManyField
    preferred_vendors = models.TextField(null=True)
    quotation_deadline = models.DateField()
    delivery_address = models.TextField()
    spoc_name = models.CharField(max_length=220, null=True)
    spoc_number = models.BigIntegerField()
    special_notes = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=220)


    def __str__(self):
        return f"RFQ {self.rfq_number} - {self.department_requesting}"



class PurchaseOrder(models.Model):
    quotation_data = models.ForeignKey('vendor_app.vendor_quotation', on_delete=models.CASCADE, null=True, related_name="purchase_orders")
    po_number = models.CharField(max_length=50, unique=True)
    po_date = models.DateField(auto_now_add=True)
    po_time = models.TimeField(auto_now_add=True)
    requested_by = models.CharField(max_length=150, null=True)
    verified_by = models.CharField(max_length=150, null=True)
    special_instructions = models.TextField(null=True, blank=True)
    po_status = models.CharField(max_length=10)

    def __str__(self):
        return f"PO {self.po_number}"