from django.db import models
from inventory_app.models import RawMaterialsStock
from purchase_app.models import RawMaterials


# Create your models here.

class RD_stock(models.Model):
    raw_materials = models.ForeignKey(RawMaterialsStock, on_delete=models.CASCADE, null=True)
    approved_stock = models.IntegerField(null=True)
    unapproved_stock = models.IntegerField(null=True)
    date = models.DateField(auto_now_add=True, null=True)
    time = models.TimeField(auto_now=True, null=True)


class RD_Unapproved_Stock(models.Model):
    raw_materials = models.ForeignKey(RawMaterials,on_delete=models.CASCADE,null=True)
    total_unapproved_stock = models.IntegerField()
    date = models.DateTimeField(auto_now=True,null=True)

