from django import forms
from .models import Ledger, Voucher, Transaction, Group, client_ledger_group
from django.forms import modelformset_factory


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'plbl_filter']
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control'}),
            'plbl_filter': forms.Select(attrs={'class': 'form-control'}),
        }

class Client_ledger_groupform(forms.ModelForm):
    class Meta:
        model = client_ledger_group
        fields = ['group', 'ledger_group']
        widgets = {
            'group': forms.Select(attrs={'class': 'form-control'}),
            'ledger_group': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Group Name'}),
        }
from django import forms
from .models import Ledger, client_ledger_group, Group

class LedgerForm(forms.ModelForm):
    combined_group = forms.ChoiceField(choices=[], required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Ledger
        fields = ['name', 'client_group', 'group']
        widgets = {
           
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ledger Name'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Combine the options of client_ledger_group and group into one dropdown
        client_groups = client_ledger_group.objects.all()
        groups = Group.objects.all()

        combined_choices = []

        # Add client_ledger_group choices with a label to distinguish them
        for cg in client_groups:
            combined_choices.append((cg.id, f"{cg.ledger_group}"))  # Show only 'ledger_group'

        # Add Group choices with a label to distinguish them
        for g in groups:
            combined_choices.append((g.id, f"{g.name}"))  # Show only 'name'

        # Set the combined choices for the dropdown
        self.fields['combined_group'].choices = combined_choices

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Get the selected ID from the combined dropdown
        combined_group_id = self.cleaned_data.get('combined_group')

        # Try to match the ID to either a client_ledger_group or a Group
        try:
            # Check if the selected ID is for a client_ledger_group
            client_group = client_ledger_group.objects.get(id=combined_group_id)
            instance.client_group = client_group
            instance.group = None
        except client_ledger_group.DoesNotExist:
            # If it's not a client_ledger_group, then it must be a Group
            instance.client_group = None
            instance.group = Group.objects.get(id=combined_group_id)

        if commit:
            instance.save()

        return instance



class VoucherForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = ['voucher_type', 'date', 'narration']
        widgets = {
            'voucher_type': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'narration': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Narration'}),
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['ledger', 'debit', 'credit']
        widgets = {
            'ledger': forms.Select(attrs={'class': 'form-control'}),
            'debit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Debit Amount'}),
            'credit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Credit Amount'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        debit = cleaned_data.get('debit', 0)
        credit = cleaned_data.get('credit', 0)

        # Ensure only one of debit or credit is entered
        if debit > 0 and credit > 0:
            raise forms.ValidationError("You can enter either Debit or Credit, not both.")
        if debit == 0 and credit == 0:
            raise forms.ValidationError("You must enter either Debit or Credit.")
        return cleaned_data

TransactionFormSet = modelformset_factory(
    Transaction,
    form=TransactionForm,
    extra=2,  # Allow 2 blank transactions by default
    widgets={
        'ledger': forms.Select(attrs={'class': 'form-control'}),
        'debit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Debit Amount'}),
        'credit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Credit Amount'}),
    }
)