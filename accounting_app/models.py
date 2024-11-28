
from django.db import models


class Group(models.Model):
    GROUP_CHOICES = [
        ('Bank Accounts', 'Bank Accounts'),
        ('Bank OCC A/C', 'Bank OCC A/C'),
        ('Bank OD A/C', 'Bank OD A/C'),
        ('Branch/Division', 'Branch/Division'),
        ('Capital A/C', 'Capital A/C'),
        ('Cash in Hand', 'Cash in Hand'),
        ('Current Assets', 'Current Assets'),
        ('current Liabilities', 'current Liabilities'),
        ('Deposits(Assets)', 'Deposits(Assets)'),
        ('Direct Expense', 'Direct Expense'),
        ('Direct Income', 'Direct Income'),
        ('Duties & Taxes','Duties & Taxes'),
        ('Expense(Direct)', 'Expense(Direct)'),
        ('Expense(Indirect)', 'Expense(Indirect)'),
        ('Fixed Assets', 'Fixed Assets'),
        ('Income(Direct)', 'Income(Direct)'),
        ('Indirect Expense', 'Indirect Expense'),
        ('Indirect Income', 'Indirect Income'),
        ('Income(Indirect)', 'Income(Indirect)'),
        ('Investments', 'Investments'),
        ('Loans & Advances(Assets)', 'Loans & Advances(Assets)'),
        ('Loan(Liabilities)', 'Loan(Liabilities)'),
        ('Misc. Expenses(Assets)', 'Misc. Expenses(Assets)'),
        ('Provisions', 'Provisions'),
        ('Purchase Accounts', 'Purchase Accounts'),
        ('Reserves And Surplus', 'Reserves And Surplus'),
        ('Retained Earnings', 'Retained Earnings'),
        ('Sales Accounts', 'Sales Accounts'),
        ('Secured Loans', 'Secured Loans'),
        ('Stock_in_Hand', 'Stock_in_Hand'),
        ('Sundry Creditors', 'Sundry Creditors'),
        ('Sundry Debtors', 'Sundry Debtors'),
        ('Suspense Accounts', 'Suspense Accounts'),
        ('Unsecured Loans ', 'Unsecured Loans'),

    ]
    plbl_filter_CHOICES = [
        ('Balance Sheet Assets', 'Balance Sheet Assets'),
        ('Balance Sheet Liabilities', 'Balance Sheet Liabilities'),
        ('P And L Direct Income ', 'P And L Direct Income'),
        ('P And L Indirect Income', 'P And L Indirect Income'),
        ('P And L Direct Expense ', 'P And L Direct Expense'),
        ('P And L Indirect Expense', 'P And L Indirect Expense'),
        ('Opening Stock', 'Opening Stock'),
        ('Closing Stock', 'Closing Stock'),

    ]
    plbl_filter = models.CharField(max_length=100,choices=plbl_filter_CHOICES)
    name = models.CharField(max_length=100, choices=GROUP_CHOICES)
    def __str__(self):
        return self.name



class client_ledger_group(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE,null=True)
    ledger_group=models.CharField(max_length=60)

    def __str__(self):
        return self.ledger_group



class Ledger(models.Model):
    name = models.CharField(max_length=100)
    client_group = models.ForeignKey(client_ledger_group, on_delete=models.CASCADE,null=True,blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE,null=True,blank=True)



class Voucher(models.Model):
    VOUCHER_TYPES = [
        ('Attendance', 'Attendance'),
        ('Contra', 'Contra'),
        ('Credit Note', 'Credit Note'),
        ('Debit Note', 'Debit Note'),
        ('Delivery Note', 'Delivery Note'),
        ('Job work in order', 'Job work in order'),
        ('Job work out order', 'Job work out order'),
        ('Journal', 'Journal'),
        ('Material In', 'Material In'),
        ('Material Out', 'Material Out'),
        ('Memorandum', 'Memorandum'),
        ('Payment', 'Payment'),
        ('PayRoll', 'PayRoll'),
        ('Physical Stock', 'Physical Stock'),
        ('Purchase', 'Purchase'),
        ('Purchase Order', 'Purchase Order'),
        ('Receipt', 'Receipt'),
        ('Receipt Note', 'Receipt Note'),
        ('Rejections In', 'Rejections In'),
        ('Rejections Out', 'Rejections Out'),
        ('Reversing Journal', 'Reversing Journal'),
        ('Sales', 'Sales'),
        ('Sales Order', 'Sales Order'),
        ('Stocks Journal', 'Stocks Journal'),

    ]
    voucher_type = models.CharField(max_length=20, choices=VOUCHER_TYPES)
    date = models.DateField()
    narration = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.voucher_type} - {self.date}"

class Transaction(models.Model):
    voucher = models.ForeignKey('Voucher', on_delete=models.CASCADE, related_name='transactions')
    ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE)
    debit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.ledger.name} | Debit: {self.debit} | Credit: {self.credit}"