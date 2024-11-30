from django import forms

from production_app.models import water_Finished_goods_category, water_Finished_Goods, damaged_Goods ,Damaged_good_category


class water_category_Form(forms.ModelForm):
    class Meta:
        model = water_Finished_goods_category
        fields = ['category_name']
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control'}),

        }


class finishedwaterForm(forms.ModelForm):
    class Meta:
        model = water_Finished_Goods
        fields = ['category','name', 'size', 'image']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'size': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        size = cleaned_data.get('size')
        name = cleaned_data.get('name')

        # Check if a water finished good with the same category and size already exists
        if water_Finished_Goods.objects.filter(category=category ,name=name ,size=size).exclude \
                (pk=self.instance.pk).exists():
            raise forms.ValidationError("Water finished goods with the same size and category already exist.")

        return cleaned_data

class DamagedForm(forms.ModelForm):
    class Meta:
        model = Damaged_good_category
        fields = ['category_name']
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control'}),

        }

class damaged_goods_Form(forms.ModelForm):
    class Meta:
        model = damaged_Goods
        fields = ['category','name', 'image', 'description']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }

class update_damaged_goods_Form(forms.ModelForm):
    class Meta:
        model = damaged_Goods
        fields = ['category','name', 'image', 'description']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }