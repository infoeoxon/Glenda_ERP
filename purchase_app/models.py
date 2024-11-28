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
