

from django import forms

from inventory_app.models import Add_RawMaterial
from purchase_app.models import RawMaterials
from vendor_app.models import vendor_register, vendor_quotation


from django import forms
from .models import vendor_quotation

class VendorQuotationForm(forms.ModelForm):
    class Meta:
        model = vendor_quotation
        fields = ['unit_Price', 'total_Price', 'discount', 'payment_terms', 'document', 'time_frame', 'special_notes']
        widgets = {
            'time_frame': forms.TextInput(attrs={'placeholder': 'Enter time frame'}),
            'special_notes': forms.TextInput(attrs={'placeholder': 'Enter any special notes'}),
            'document': forms.ClearableFileInput(attrs={'multiple': True}),
        }

class VendorRegisterForm(forms.ModelForm):
    materials_name = forms.ModelMultipleChoiceField(
        queryset=Add_RawMaterial.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = vendor_register
        fields = [
            'company_name', 'vendor_district', 'vendor_state', 'vendor_country',
            'vendor_pincode', 'pan_yes_or_no', 'vendor_PANNBR',
            'vendor_Street', 'vendor_Landmark', 'materials_name', 'vendor_Building'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'vendor_district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'District'}),
            'vendor_state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'vendor_country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'vendor_pincode': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'}),
            'pan_yes_or_no': forms.Select(attrs={'class': 'form-control'}),
            'vendor_PANNBR': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PAN Number'}),
            'vendor_Street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street'}),
            'vendor_Landmark': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Landmark'}),
            'vendor_Building': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Building'}),
        }