from Glenda_App.models import Menu, SubMenu
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser

from register_app.models import department, designation, MenuPermissions
from django.core.validators import RegexValidator, EmailValidator


class department_Form(forms.ModelForm):
    class Meta:
        model = department
        fields = ['dept_Name']
        widgets = {
            'dept_Name': forms.Select(attrs={'class': 'form-control'}),

        }


class designation_Form(forms.ModelForm):
    class Meta:
        model = designation
        fields = ['user_type', 'dept']
        widgets = {
            'user_type': forms.TextInput(attrs={'class': 'form-control'}),
            'dept': forms.Select(attrs={'class': 'form-control'}),
        }


class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'email',
            'phone_number',
            'designation',
            'department',
            'joining_date',
            'name',
            'image',  # Added profile_photo field
            'password1',
            'password2',

        ]
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),
            'designation': forms.Select(attrs={
                'class': 'form-control'
            }),
            'department': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_department'
            }),
            'joining_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'  # Custom widget for file input
            }),  # Added profile_photo widget
        }

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
    )








class CustomLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
            'style': 'border-radius: 5px; padding: 10px;',  # custom styling
            'autocomplete': 'email',
            'aria-label': 'Email'
        }),
        error_messages={
            'required': 'Please enter your email address.',
            'invalid': 'Enter a valid email address.'
        }
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'style': 'border-radius: 5px; padding: 10px;',  # custom styling
            'autocomplete': 'current-password',
            'aria-label': 'Password'
        }),
        error_messages={
            'required': 'Please enter your password.'
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        # You can add any additional validation here if needed
        # For example, checking if email is in a specific domain

        return cleaned_data


class PermissionForm(forms.ModelForm):
    menu = forms.ModelChoiceField(queryset=Menu.objects.all(), required=False, label="Menu")
    sub_menu = forms.ModelChoiceField(queryset=SubMenu.objects.none(), required=False, label="Sub Menu")  # Start with no submenus

    class Meta:
        model = MenuPermissions
        fields = ['menu', 'sub_menu']  # Updated fields list

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'menu' in self.data:
            try:
                menu_id = int(self.data.get('menu'))
                self.fields['sub_menu'].queryset = SubMenu.objects.filter(menu_id=menu_id).order_by('title')
            except (ValueError, TypeError):
                pass  # If the menu is not valid, do nothing
        elif self.instance.pk:
            self.fields['sub_menu'].queryset = self.instance.menu.submenus.order_by('title')