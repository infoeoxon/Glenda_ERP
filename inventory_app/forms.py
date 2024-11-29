from django import forms
from django.utils import timezone

from inventory_app.models import RawMaterialsStock, Finished_Goods_Stock, Damaged_Goods_Stock, Finished_Goods_Request, \
    Raw_material_request, Raw_material_allocate, Finished_Goods_allocate, AddCategory, Add_RawMaterial, \
    Purchase_request_raw_material, Purchase_request_semi_finished, Add_semi_finished_good, Add_finished_good
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


# new forms
class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = AddCategory
        fields = ['category_name', 'material_type']
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Category Name'}),
            'material_type': forms.Select(attrs={'class': 'form-control'}),  # Dropdown for material type
        }


class AddRawMaterialForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=AddCategory.objects.filter(material_type='Raw Materials'),  # Show categories for 'Raw Materials'
        empty_label="Select Category",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Add_RawMaterial
        fields = ['category', 'name', 'size', 'color', 'image']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'size': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class PurchaseRequestRawMaterialForm(forms.ModelForm):
    # Override the fields to include dropdown widgets where necessary
    department = forms.ModelChoiceField(
        queryset = department.objects.filter(dept_Name='Purchase'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Department"
    )
    category = forms.ModelChoiceField(
        queryset=AddCategory.objects.filter(material_type='Raw Materials'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Category"
    )
    product_name = forms.ModelChoiceField(
        queryset=Add_RawMaterial.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Product"
    )

    class Meta:
        model = Purchase_request_raw_material
        fields = ['department', 'category', 'product_name', 'required_date', 'quantity_required', 'remarks']

        widgets = {
            'required_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'quantity_required': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter remarks'}),
        }


class PurchaseRequestSemiFinishedForm(forms.ModelForm):
    # Filtered Department Dropdown
    department = forms.ModelChoiceField(
        queryset=department.objects.filter(dept_Name__in=['Production', 'Purchase']),  # Filter for Production or Purchase
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Department"
    )
    # Category Dropdown (Filtered for Semi-Finished Goods)
    category = forms.ModelChoiceField(
        queryset=AddCategory.objects.filter(material_type='Semi Finished Goods'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Category"
    )
    # Product Name Dropdown (Dynamically Populated in the View)
    name = forms.ModelChoiceField(
        queryset=Add_semi_finished_good.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Product"
    )

    class Meta:
        model = Purchase_request_semi_finished
        fields = ['department', 'category', 'name', 'required_date', 'quantity_required', 'remarks']

        widgets = {
            'required_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'quantity_required': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter remarks'}),
        }


class Add_finished_Form(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=AddCategory.objects.filter(material_type='Finished Goods'),  # Show categories for 'Raw Materials'
        empty_label="Select Category",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Add_finished_good
        fields = ['category', 'name','size','image' ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'size': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Size'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Image'}),
        }



class Add_semi_finished_Form(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=AddCategory.objects.filter(material_type='Semi Finished Goods'),  # Show categories for 'Raw Materials'
        empty_label="Select Category",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Add_semi_finished_good
        fields = ['category', 'name','size','image' ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'size': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Size'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Image'}),
        }