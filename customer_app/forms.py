
import re
from django import forms

from customer_app.models import customer_registration


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = customer_registration
        fields = ['name' ,'address' ,'pincode' ,'state' ,'district' ,'email' ,'GST_yes_or_no' ,'GST_number'
                  ,'pan_yes_or_no' ,'PAN_number' ,'phone_number']
        widgets = {

            'name' :forms.TextInput(attrs={'class' :'form-control'}),

            'address' :forms.TextInput(attrs={'class' :'form-control'}),
            'pincode' :forms.TextInput(attrs={'class' :'form-control'}),
            'state' :forms.TextInput(attrs={'class' :'form-control'}),
            'district' :forms.TextInput(attrs={'class' :'form-control'}),
            'email' :forms.EmailInput(attrs={'class' :'form-control'}),
            'GST_yes_or_no' :forms.Select(attrs={'class' :'form-control'}),
            'GST_number' :forms.TextInput(attrs={'class' :'form-control'}),
            # 'PAN_CHOICES':forms.TextInput(attrs={'class':'form-control'}),
            'pan_yes_or_no' :forms.Select(attrs={'class' :'form-control'}),
            'PAN_number' :forms.TextInput(attrs={'class' :'form-control'}),
            'phone_number' :forms.TextInput(attrs={'class' :'form-control'}),

        }
        def clean_GST_number(self):
            GST_number = self.cleaned_data.get('GST_number')
            if GST_number and not re.match(r'^[A-Z]{7}[0-9]{6}[A-Z]$', GST_number):
                raise forms.ValidationError \
                    ("GST number must be in the format: XXXXXXX0000X0X0 (7 letters, 6 digits, 2 letter).")
            return GST_number

        def clean_phone_number(self):
            phone_number = self.cleaned_data.get('phone_number')
            if phone_number and (len(str(phone_number)) != 10 or not str(phone_number).isdigit()):
                raise forms.ValidationError("Phone number must be 10 digits long and numeric.")
            return phone_number

        def clean_PAN_number(self):
            PAN_number = self.cleaned_data.get('PAN_number')
            if PAN_number and not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', PAN_number):
                raise forms.ValidationError \
                    ("PAN number must be in the format: XXXXX0000X (5 letters, 4 digits, 1 letter).")
            return PAN_number

        def clean(self):
            cleaned_data = super().clean()