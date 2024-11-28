
from django import forms
from django.core.exceptions import ValidationError
from purchase_app.models import RawMaterialCategory, RawMaterials


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
            if RawMaterials.objects.filter(category=category, name=name, size=size).exclude(pk=self.instance.pk).exists():
                raise ValidationError("Raw material with the same size and category already exists.")

        return cleaned_data