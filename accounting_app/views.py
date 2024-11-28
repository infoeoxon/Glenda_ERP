from django.shortcuts import render, redirect, get_object_or_404

from .form import VoucherForm, TransactionForm, LedgerForm, TransactionFormSet, GroupForm, Client_ledger_groupform
from .models import Voucher, Transaction, Ledger
from django.forms import modelformset_factory

# Create your views here.

def add_group(request):
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_group')  # Adjust the redirection URL
    else:
        form = GroupForm()
    return render(request, 'accounting/group.html', {'form': form})

def add_client_ledger_group(request):
    if request.method == "POST":
        form = Client_ledger_groupform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_group')  # Adjust the redirection URL
    else:
        form = Client_ledger_groupform()
    return render(request, 'accounting/client_add_group.html', {'form': form})


def add_ledger(request):
    if request.method == "POST":
        form = LedgerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ledger_list')  # Adjust the redirection URL
    else:
        form = LedgerForm()
    return render(request, 'accounting/add_ledger.html', {'form': form})

def ledger_list(request):
    ledgers = Ledger.objects.all()
    return render(request, 'accounting/ledger_list.html', {'ledgers': ledgers})


# views.py
def create_voucher(request):
    if request.method == "POST":
        voucher_form = VoucherForm(request.POST)
        transaction_formset = TransactionFormSet(request.POST, queryset=Transaction.objects.none())

        if voucher_form.is_valid() and transaction_formset.is_valid():
            voucher = voucher_form.save()
            for form in transaction_formset:
                transaction = form.save(commit=False)
                transaction.voucher = voucher
                transaction.save()
            return redirect('voucher_list')
        else:
            # Display errors
            return render(request, 'accounting/create_voucher.html', {
                'voucher_form': voucher_form,
                'transaction_formset': transaction_formset,
            })
    else:
        voucher_form = VoucherForm()
        transaction_formset = TransactionFormSet(queryset=Transaction.objects.none())

    return render(request, 'accounting/create_voucher.html', {
        'voucher_form': voucher_form,
        'transaction_formset': transaction_formset,
    })


def voucher_detail(request, voucher_id):
    voucher = get_object_or_404(Voucher, id=voucher_id)
    transactions = Transaction.objects.filter(voucher=voucher)

    total_debit = sum(transaction.debit for transaction in transactions)
    total_credit = sum(transaction.credit for transaction in transactions)

    return render(request, 'accounting/voucher_detail.html', {
        'voucher': voucher,
        'transactions': transactions,
        'total_debit': total_debit,
        'total_credit': total_credit
    })

def voucher_list(request):
    vouchers = Voucher.objects.all()  # Retrieve all vouchers from the database
    return render(request, 'accounting/voucher_list.html', {
        'vouchers': vouchers
    })