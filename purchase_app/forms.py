from django import forms
from django.core.exceptions import ValidationError

from inventory_app.models import Add_RawMaterial, AddCategory
from purchase_app.models import RawMaterialCategory, RawMaterials, RFQ_raw_materials
from vendor_app.models import vendor_register


class CategoryForm(forms.ModelForm):
    class Meta:
        model = RawMaterialCategory
        fields = ['category_name']
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class RawMaterialForm(forms.ModelForm):
    class Meta:
        model = RawMaterials  # Corrected model name
        fields = ['category', 'name', 'size', 'color', 'image']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'size': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        size = cleaned_data.get('size')
        name = cleaned_data.get('name')

        if name and size and category:
            if RawMaterials.objects.filter(category=category, name=name, size=size).exclude(
                    pk=self.instance.pk).exists():
                raise ValidationError("Raw material with the same size and category already exists.")

        return cleaned_data


# new forms starts here

class RFQRawMaterialsForm(forms.ModelForm):
    # Material Category Dropdown (Filtered by Raw Materials)
    material_category = forms.ModelChoiceField(
        queryset=AddCategory.objects.filter(material_type='Raw Materials'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Material Category"
    )
    # Material Name Dropdown
    material_name = forms.ModelChoiceField(
        queryset=Add_RawMaterial.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Material Name"
    )
    # Vendor List as Multiple Choice (Rendered Separately in Template)
    vendor_list = forms.ModelMultipleChoiceField(
        queryset=vendor_register.objects.filter(
            status='Approved',
            materials_name__category__material_type='Raw Materials'
        ).distinct(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'vendor-checkbox'}),
        required=False,
    )

    class Meta:
        model = RFQ_raw_materials
        fields = [
            'material_category',
            'material_name',
            'quantity_needed',
            'batch_requirements',
            'quality_standards',
            'expected_delivery_date',
            'quotation_deadline',
            'delivery_address',
            'special_notes',
            'spoc_name',
            'spoc_number',
        ]
        exclude = ['vendor_list']  # Exclude vendor_list from automatic rendering
        widgets = {
            'quantity_needed': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity needed'}),
            'batch_requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter batch requirements'}),
            'quality_standards': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'expected_delivery_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'quotation_deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'delivery_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter delivery address'}),
            'special_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter special notes'}),
            'spoc_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter SPOC name'}),
            'spoc_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter SPOC number'}),
        }

