from datetime import timedelta

from django.db import models
from production_app.models import damaged_Goods
from production_app.models import water_Finished_Goods, water_Finished_goods_category
from purchase_app.models import RawMaterials, RawMaterialCategory
from register_app.models import department


# Create your models here.

class RawMaterialsStock(models.Model):
    raw_materials = models.ForeignKey(RawMaterials, related_name='stocks', on_delete=models.CASCADE, null=True)
    stock = models.IntegerField(null=True)  # Stock quantity
    date = models.DateField(auto_now_add=True)  # Only set on creation
    time = models.TimeField(auto_now_add=True, null=True)  # Only set on creation
    status = models.CharField(max_length=300, null=True, blank=True)
    response = models.TextField(default='', null=True, blank=True)
    remarks = models.TextField(default='', null=True, blank=True)


class Finished_Goods_Stock(models.Model):
    finished_goods = models.ForeignKey(water_Finished_Goods, related_name='stocks', on_delete=models.CASCADE, null=True)
    stock = models.IntegerField(null=True)  # Stock quantity
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True, null=True)
    remarks = models.TextField(default='', blank=True)
    quantity = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.finished_goods.name} - {self.stock} units"


class Damaged_Goods_Stock(models.Model):
    damaged = models.ForeignKey(damaged_Goods, related_name='stocks', on_delete=models.CASCADE, null=True)
    stock = models.IntegerField(null=True)
    date = models.DateField(auto_now_add=True, null=True)
    time = models.TimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.damaged.name} - {self.stock} units"


class Finished_Goods_Request(models.Model):
    department = models.ForeignKey(department, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(water_Finished_goods_category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.ForeignKey(water_Finished_Goods, on_delete=models.CASCADE, null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    input_date = models.DateField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True, blank=True)
    remarks = models.TextField(default='', blank=True)
    status = models.CharField(max_length=300, null=True, blank=True)
    response = models.TextField(default='', null=True, blank=True)

    def __str__(self):
        return f"Request to {self.department.dept_Name} for {self.stock} units of {self.name.name}"


class Raw_material_request(models.Model):
    department = models.ForeignKey(department, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(RawMaterialCategory, on_delete=models.CASCADE, null=True)
    name = models.ForeignKey(RawMaterials, on_delete=models.CASCADE, null=True)
    stock = models.IntegerField(null=True)
    input_date = models.DateField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(default='')
    status = models.CharField(max_length=155, null=True)
    response = models.TextField(default='')

    def _str_(self):
        return f"request to {self.department.dept_Name} for {self.stock} units of {self.name.name}"


class Raw_material_allocate(models.Model):
    raw_material = models.ForeignKey(RawMaterials, on_delete=models.CASCADE, null=True)
    stock = models.IntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(null=True)


class Finished_Goods_allocate(models.Model):
    stock = models.IntegerField(null=True)
    date = models.DateTimeField(auto_now=True)
    remarks = models.TextField(default='')
    finished_good = models.ForeignKey(water_Finished_Goods, on_delete=models.CASCADE, null=True)


#  new codes start's here

class AddCategory(models.Model):
    category_name = models.CharField(max_length=150, null=True)
    MATERIAL_TYPE_CHOICES = [
        ('Raw Materials', 'Raw Materials'),
        ('Finished Goods', 'Finished Goods'),
        ('Semi Finished Goods', 'Semi Finished Goods'),
    ]
    material_type = models.CharField(max_length=50, choices=MATERIAL_TYPE_CHOICES, null=True)

    def __str__(self):
        return self.category_name


class Add_RawMaterial(models.Model):
    category = models.ForeignKey(AddCategory, on_delete=models.CASCADE, null=True, related_name="category_raw_materials")
    name = models.CharField(max_length=150, null=True, unique=True)
    size = models.CharField(max_length=150, null=True)
    color = models.CharField(max_length=150, null=True)
    image = models.ImageField(upload_to='images/', null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True, null=True)
    total_stock = models.IntegerField(default=0)  # Field to track total stock
    total_damaged_stock = models.IntegerField(default=0)


    def __str__(self):
        return self.name


class Add_finished_good(models.Model):
    category = models.ForeignKey(
        AddCategory, on_delete=models.CASCADE, null=True, related_name="finished_goods_category"
    )
    name = models.CharField(max_length=150, null=True, unique=True)
    size = models.CharField(max_length=150, null=True, unique=True)
    unit = models.CharField(max_length=150, null=True, unique=True)
    unit_define = models.IntegerField(null=True)
    image = models.ImageField(upload_to='images/', null=True)
    date = models.DateField(auto_now_add=True, null=True)
    time = models.TimeField(auto_now_add=True, null=True)
    total_stock = models.IntegerField(default=0)
    total_damaged = models.IntegerField(default=0)


class Add_semi_finished_good(models.Model):
    category = models.ForeignKey(
        AddCategory, on_delete=models.CASCADE, null=True, related_name="semi_finished_goods_category"
    )
    name = models.CharField(max_length=150, null=True, unique=True)
    type = models.ForeignKey(
        AddCategory, on_delete=models.CASCADE, null=True, related_name="semi_finished_goods_type"
    )
    size = models.CharField(max_length=150, null=True, unique=True)
    unit = models.CharField(max_length=150, null=True, unique=True)
    unit_define = models.IntegerField(null=True)
    image = models.ImageField(upload_to='images/', null=True)
    total_stock = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

class RawMaterialStock(models.Model):
    raw_materials = models.ForeignKey(Add_RawMaterial, on_delete=models.CASCADE, null=True, related_name="stock_raw_materials")
    stock_entry = models.IntegerField(default=0)
    damaged_entry_stock = models.IntegerField(default=0)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now_add=True)


class Purchase_request_raw_material(models.Model):
    department = models.ForeignKey(department,on_delete=models.CASCADE,null=True,related_name='department_request')
    category = models.ForeignKey(AddCategory,on_delete=models.CASCADE,null=True,related_name='category_request')
    product_name = models.ForeignKey(Add_RawMaterial, on_delete=models.CASCADE, null=True, related_name='product_request')
    quantity_required = models.IntegerField()
    required_date = models.DateField()
    remarks = models.TextField()
    requested_by = models.CharField(max_length=150, null=True)  # Name and designation of the requestor (foreign key)
    verified_by = models.CharField(max_length=150, null=True)  # Name and designation of the verifier (foreign key)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=220)


class Purchase_request_semi_finished(models.Model):
    department = models.ForeignKey(department,on_delete=models.CASCADE,null=True,related_name='department_semi_request')
    category = models.ForeignKey(AddCategory,on_delete=models.CASCADE,null=True,related_name='category_request_semi')
    product_name = models.ForeignKey(Add_semi_finished_good, on_delete=models.CASCADE, null=True, related_name='product_request_semi')
    quantity_required = models.IntegerField()
    required_date = models.DateField()
    remarks = models.TextField()
    requested_by = models.CharField(max_length=150, null=True)  # Name and designation of the requestor (foreign key)
    verified_by = models.CharField(max_length=150, null=True)  # Name and designation of the verifier (foreign key)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=220)