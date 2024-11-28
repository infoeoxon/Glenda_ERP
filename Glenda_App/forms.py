

from django import forms

from Glenda_App.models import Menu, SubMenu


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['title', 'icon']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Menu Title'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Icon Class (e.g., ri-pages-line)'
            }),
        }

class SubMenuForm(forms.ModelForm):
    class Meta:
        model = SubMenu
        fields = ['menu', 'title', 'url_name']
        widgets = {
            'menu': forms.Select(attrs={
                'class': 'form-control',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Submenu Title'
            }),
            'url_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter URL Name (e.g., raw_materials)'
            }),
        }
