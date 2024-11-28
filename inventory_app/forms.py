from django import forms
from django.utils import timezone

from inventory_app.models import RawMaterialsStock, Finished_Goods_Stock, Damaged_Goods_Stock, Finished_Goods_Request, \
    Raw_material_request, Raw_material_allocate, Finished_Goods_allocate
from register_app.models import department


class Raw_materials_StockForm(forms.ModelForm):
    class Meta:
        model = RawMaterialsStock
        fields = ['stock','remarks']
        widgets = {
            'stock': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Remarks'}),

        }


class Finished_Goods_StockForm(forms.ModelForm):
    class Meta:
        model = Finished_Goods_Stock
        fields = ['stock', 'remarks']
        widgets = {
            'stock': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Remarks'}),
        }


class Damaged_Goods_StockForm(forms.ModelForm):
    class Meta:
        model = Damaged_Goods_Stock
        fields = ['stock']
        widgets = {
            'stock': forms.TextInput(attrs={'class': 'form-control'}),

        }


class Finished_Goods_RequestForm(forms.ModelForm):
    class Meta:
        model = Finished_Goods_Request
        fields = [
            'department',
            'category',
            'name',
            'stock',
            'input_date',
            'remarks',
            'response',
        ]
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Department'}),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Category'}),
            'name': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'stock': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Required Quantity'}),
            'input_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Date',
            }),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Remarks'}),
            'response': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Reason for Decline', 'style': 'display:none;'}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = department.objects.filter(dept_Name="Production")




class Raw_materials_requestForm(forms.ModelForm):
    class Meta:
        model = Raw_material_request
        fields = [
            'department',
            'category',
            'name',
            'stock',
            'input_date',
            'remarks',
        ]

        widgets = {
            'department': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Department'}),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Category'}),
            'name': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'stock': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Required Quantity'}),
            'input_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Date'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Remarks'}),
            'response': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Reason for Decline', 'style': 'display:none;'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = department.objects.filter(dept_Name="Purchase")


class Raw_material_allocate_Form(forms.ModelForm):
    class Meta:
        model = Raw_material_allocate
        fields = ['stock','remarks']
        widgets = {
            'stock': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Remarks'}),

        }


class Finished_Goods_allocateForm(forms.ModelForm):
    class Meta:
        model = Finished_Goods_allocate
        fields = ['stock', 'remarks']
        widgets = {
            'stock': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Remarks'}),
        }