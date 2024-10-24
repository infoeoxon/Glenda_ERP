from django import forms
from .models import EmployeeDetails

class EmployeeDetailsForm(forms.ModelForm):
    class Meta:
        model = EmployeeDetails
        fields = ['emergency_contact_number','aadhar_no','street','pincode','state','country','landmark','district','salary_information']
        widgets = {
            'emergency_contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'aadhar_no': forms.TextInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode':forms.TextInput(attrs={'class': 'form-control'}),
            'state':forms.TextInput(attrs={'class': 'form-control'}),
            'country':forms.TextInput(attrs={'class': 'form-control'}),
            'landmark':forms.TextInput(attrs={'class': 'form-control'}),
            'district':forms.TextInput(attrs={'class': 'form-control'}),
            'salary_information':forms.TextInput(attrs={'class': 'form-control'}),
        }