
from django import forms
from logistics_app.models import dealer_reg, DispatchAdvice, Driver, Privatevehicle, Route, Route_Plan, Vehicle, Vehicle_Maintenance, trackorder
from django.utils import timezone
from django.core.exceptions import ValidationError
import re
from register_app.models import CustomUser

class DealerForm(forms.ModelForm):
    class Meta:
        model = dealer_reg
        fields = ['dealer_name','dealer_nbr','dealer_address']
        widgets = {
            'dealer_name': forms.TextInput(attrs={'class':'form-control'}),
            'dealer_nbr':forms.TextInput(attrs={'class':'form-control'}),
            'dealer_address':forms.TextInput(attrs={'class':'form-control'}),
        }

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['user', 'license_number', 'aadhaar_number', 'phone_number', 'license_exp_date', 'upload_license','remarks',
            'ratings']
        today = timezone.now().date()

        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'aadhaar_number': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'license_exp_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': today + timezone.timedelta(days=1)  # Set min to tomorrow
            }),
            'upload_license': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control'}),
            'ratings': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(DriverForm, self).__init__(*args, **kwargs)
        # Filter user queryset to include users with the designation 'Driver'
        self.fields['user'].queryset = CustomUser.objects.filter(designation__user_type='Driver')

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not re.match(r'^\+?1?\d{9,15}$', phone_number):  # Adjust regex as per your requirements
            raise ValidationError("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
        return phone_number

    def clean_aadhaar_number(self):
        aadhaar_number = self.cleaned_data.get('aadhaar_number')
        if not re.match(r'^\d{12}$', aadhaar_number):  # Aadhaar number must be 12 digits
            raise ValidationError("Aadhaar number must be 12 digits long.")
        return aadhaar_number

    def clean_license_number(self):
        license_number = self.cleaned_data.get('license_number')
        if not license_number or not re.match(r'^[A-Z]{2}\d{13}$', license_number):  # Example format: 'HR0619850034761'
            raise ValidationError(
                "License number must start with two letters followed by 13 digits (e.g., 'HR0619850034761').")
        return license_number


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'vehicle_name',
            'vehicle_nbr',
            'vehicle_img',
            'vehicle_insurance_date',
            'vehicle_taxes_date',
            'vehicle_fasttag',
            'vehicle_pollution_date',
            'vehicle_capacity',
            'vehicle_rate'
        ]
        today = timezone.now().date()
        widgets = {
            'vehicle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_nbr': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_img': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'vehicle_insurance_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': today + timezone.timedelta(days=1)  # Set min to tomorrow
            }),
            'vehicle_taxes_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': today + timezone.timedelta(days=1)  # Set min to tomorrow
            }),
            'vehicle_fasttag': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_pollution_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': today + timezone.timedelta(days=1)  # Set min to tomorrow
            }),
            'vehicle_capacity':forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_rate':forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_vehicle_nbr(self):
        vehicle_nbr = self.cleaned_data.get('vehicle_nbr')
        errors = []

        # Check if vehicle number is empty
        if not vehicle_nbr:
            errors.append("Vehicle number is required.")
        else:
            # Check length
            if len(vehicle_nbr) < 5 or len(vehicle_nbr) > 15:
                errors.append("Vehicle number must be between 5 and 15 characters long.")

            # Check if it's alphanumeric
            if not vehicle_nbr.isalnum():
                errors.append("Vehicle number must be alphanumeric.")

            # Check for spaces
            if ' ' in vehicle_nbr:
                errors.append("Vehicle number must not contain spaces.")

        # Check for uniqueness
        if Vehicle.objects.filter(vehicle_nbr=vehicle_nbr).exists():
            errors.append("This vehicle number is already in use. Please enter a unique number.")

        if errors:
            raise forms.ValidationError(errors)

        return vehicle_nbr


# forms.py



class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['route_name', 'starting_point', 'ending_point', 'total_distance']
        widgets = {
            'route_name': forms.TextInput(attrs={'class': 'form-control'}),
            'starting_point': forms.TextInput(attrs={'class': 'form-control'}),
            'ending_point': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),  # Keep it readonly
            'total_distance': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(RouteForm, self).__init__(*args, **kwargs)
        self.fields['ending_point'].widget.attrs.update({'placeholder': 'Select ending point on map'})



class RoutePlanForm(forms.ModelForm):
    class Meta:
        model = Route_Plan
        fields = ['vehicle', 'route', 'driver', 'date', 'time']
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'route': forms.Select(attrs={'class': 'form-control', 'id': 'id_route'}),
            'driver': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'percasecost':forms.TextInput(attrs={'class':'form-control'}),
            'dealer': forms.Select(attrs={'class':'form-control'}),
            'status':forms.TextInput(attrs={'class':'form-control'}),

        }

    # Fields for route details
    route_distance = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control', 'placeholder': 'Route Distance'})
    )
    route_starting_point = forms.CharField(  # Updated field name
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control', 'placeholder': 'Starting Destination'})
    )
    route_ending_point = forms.CharField(  # Updated field name
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control', 'placeholder': 'Ending Destination'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['route_distance'].initial = ''
        self.fields['route_starting_point'].initial = ''  # Updated field name
        self.fields['route_ending_point'].initial = ''  # Updated field name

        if 'route' in self.data:
            try:
                route_id = int(self.data.get('route'))
                route = Route.objects.get(id=route_id)
                self.fields['route_distance'].initial = route.total_distance  # Matches model field
                self.fields['route_starting_point'].initial = route.starting_point  # Matches model field
                self.fields['route_ending_point'].initial = route.ending_point  # Matches model field
            except (ValueError, Route.DoesNotExist):
                pass


class VehicleMaintenanaceForm(forms.ModelForm):
    class Meta:
        model = Vehicle_Maintenance
        fields = ['vehicle', 'TypeofMaintenance', 'amount', 'Remarks']
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'TypeofMaintenance': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
            'Remarks': forms.TextInput(attrs={'class': 'form-control'}),

        }


class DispatchAdviceForm(forms.ModelForm):
    class Meta:
        model = DispatchAdvice
        fields = ['name','quantity','destination','route_plan','user','date','dealer']
        widgets = {
            'name':forms.Select(attrs={'class':'form-control'}),
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
            'destination':forms.TextInput(attrs={'class':'form-control'}),
            'route_plan':forms.Select(attrs={'class':'form-control'}),
            'user':forms.Select(attrs={'class':'form-control'}),
            'date':forms.DateInput(attrs={'class':'form-control'}),
            'dealer':forms.Select(attrs={'class':'form-control'}),
          
        }

class PrivatevehicleForm(forms.ModelForm):
    class Meta:
        model = Privatevehicle
        fields=['vehiclename','driver','date','capacity','img','remarks','nbr']
        widgets = {
           'vehiclename': forms.TextInput(attrs={'class':'form-control'}),
           'driver':forms.TextInput(attrs={'class':'form-control'}),
           'date':forms.DateInput(attrs={'class':'form-control'}),
           'capacity':forms.TextInput(attrs={'class':'form-control'}),
            'img':forms.ClearableFileInput(attrs={'class':'form-control'}),
           'remarks':forms.TextInput(attrs={'class':'form-control'}),
           'nbr':forms.TextInput(attrs={'class':'form-control'}),
        }

class trackorderForm(forms.ModelForm):
    class Meta:
        model=trackorder
        fields=['name','number','product','quantity','dealer','date','total','status']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'number': forms.TextInput(attrs={'class':'form-control'}),
            'product': forms.Select(attrs={'class':'form-control'}),
            'quantity': forms.TextInput(attrs={'class':'form-control'}),
            'dealer': forms.Select(attrs={'class':'form-control'}),
            'date':forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'total': forms.TextInput(attrs={'class':'form-control'}),
            'status':forms.TextInput(attrs={'class':'form-control'}),
            # 'view': forms.Select(attrs={'class':'form-control'}),
    }

