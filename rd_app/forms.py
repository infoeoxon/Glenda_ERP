from django import forms

from rd_app.models import RD_stock


class RD_approvalForm(forms.ModelForm):
    class Meta:
        model = RD_stock
        fields = ['approved_stock']
        widgets = {
            'approved_stock': forms.TextInput(attrs={'class': 'form-control'}),

        }