from datetime import date, timedelta
from django import forms
from django.core.exceptions import ValidationError
from .models import EmployeeDetails,RequestLeave,Payroll,Resignation,Remarks
from django.core.cache import cache
from django.core.files.base import File
from django.core.files.base import ContentFile


class EmployeeDetailsForm(forms.ModelForm):
    class Meta:
        model = EmployeeDetails
        fields = [
            'id_proof_type', 'other_id_proof_type', 'id_proof_type_number', 'id_proof_file',
            'street', 'pincode', 'state', 'country', 'landmark', 'district', 'date_of_birth',
            'employee_blood_groups', 'qualification', 'qualification_file', 'experience',
            'experience_file', 'joining_date', 'pcc', 'nsr', 'validity', 'building',
            'gender', 'resume', 'bank_details'
        ]

        widgets = {
            'id_proof_type': forms.Select(attrs={'class': 'form-control'}),
            'other_id_proof_type': forms.Select(attrs={'class': 'form-control'}),
            'id_proof_type_number': forms.TextInput(attrs={'class': 'form-control'}),
            'id_proof_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'landmark': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'employee_blood_groups': forms.Select(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'qualification_file': forms.FileInput(attrs={'class': 'form-control'}),
            'experience': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_file': forms.FileInput(attrs={'class': 'form-control'}),
            'joining_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'pcc': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'nsr': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'validity': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'building': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bank_details': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Check if files are available in initial data
        for field in self.fields:
            file_data = self.initial.get(field)
            if file_data:
                self.fields[field].initial = file_data

    def clean_joining_date(self):
        selected_date = self.cleaned_data['joining_date']
        today = date.today()

        # Validate the selected date
        if selected_date < date(today.year, today.month - 1, 1):
            raise ValidationError("The joining date cannot be earlier than the first day of the previous month.")
        return selected_date

class BasicForm(forms.ModelForm):
    class Meta:
        model = EmployeeDetails
        fields = ['basic','employee_esi_no','pf_no']

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = RequestLeave
        fields = ['leave_type','start_date','end_date','reason',]
        widgets = {
            'leave_type': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = ['hra', 'da', 'ot', 'leave_plus', 'medical', 'insurance', 'ta', 'food_allowance', 'canteen_expense', 'pf', 'esi', 'bonuses', 'pay_date']
        widgets = {
            'hra': forms.TextInput(attrs={'class': 'form-control'}),
            'da': forms.TextInput(attrs={'class': 'form-control'}),
            'ot': forms.TextInput(attrs={'class': 'form-control'}),
            'leave_plus': forms.TextInput(attrs={'class': 'form-control'}),
            'medical': forms.TextInput(attrs={'class': 'form-control'}),
            'insurance': forms.TextInput(attrs={'class': 'form-control'}),
            'ta': forms.TextInput(attrs={'class': 'form-control'}),
            'food_allowance': forms.TextInput(attrs={'class': 'form-control'}),
            'canteen_expense': forms.TextInput(attrs={'class': 'form-control'}),
            'pf': forms.TextInput(attrs={'class': 'form-control'}),
            'esi': forms.TextInput(attrs={'class': 'form-control'}),
            'bonuses': forms.TextInput(attrs={'class': 'form-control'}),
            'pay_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class ResignationForm(forms.ModelForm):
    class Meta:
        model = Resignation
        fields = ['date','remarks','reason']
        widgets = {
            'date':forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'remarks':forms.TextInput(attrs={'class':'form-control'}),
            'reason':forms.TextInput(attrs={'class':'form-control'}),
        }

class RemarksForm(forms.ModelForm):
    class Meta:
        model = Remarks
        fields = ['date','remarks','reason','ratings','suggest_to_improve']
        widgets = {
            'date':forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'remarks':forms.TextInput(attrs={'class':'form-control'}),
            'reason':forms.TextInput(attrs={'class':'form-control'}),
            'ratings':forms.Select(attrs={'class': 'form-control'}),
            'suggest_to_improve':forms.TextInput(attrs={'class':'form-control'})
        }