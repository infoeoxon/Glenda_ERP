from datetime import datetime, date

from django.db import models
from register_app.models import CustomUser
from django.core.exceptions import ValidationError
from decimal import Decimal
import re

class EmployeeDetails(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='employeedetails')
    status = models.CharField(max_length=50, choices=[('verified', 'Verified'), ('approved', 'Approved'), ('pending', 'Pending'), ('rejected', 'Rejected')], default='pending')
    joining_date = models.DateField(null=True, blank=True)
    basic = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    street = models.CharField(max_length=150, null=True, blank=True)
    pincode = models.CharField(max_length=9, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    landmark = models.CharField(max_length=100, null=True, blank=True)
    building = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=120, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    BloodGroupTypes = (
        ('AB+', 'AB+'),
        ('B+', 'B+'),
        ('A+', 'A+'),
        ('O+', 'O+'),
        ('AB-', 'AB-'),
        ('B-', 'B-'),
        ('A-', 'A-'),
        ('O-', 'O-'),
    )

    employee_blood_groups = models.CharField(max_length=100, choices=BloodGroupTypes, default='AB+', blank=True)
    pf_no = models.CharField(max_length=22, unique=True, null=True, blank=True)  # Allow NULL and blank
    employee_esi_no = models.CharField(max_length=17, unique=True, null=True, blank=True)  # Allow NULL and blank
    qualification = models.CharField(max_length=100, blank=True)
    qualification_file = models.FileField(upload_to='qualification_files/', null=True, blank=True)
    experience = models.CharField(max_length=100, blank=True)
    experience_file = models.FileField(upload_to='experience_files/', null=True, blank=True)
    id_proof_types = (
        ('AADHAR', 'AADHAR'),
        ('PASSPORT', 'PASSPORT'),
        ('PAN CARD', 'PAN CARD'),
        ('OTHERS', 'OTHERS')
    )
    other_id_proof_types = (
        ('DRIVING LICENSE', 'DRIVING LICENSE'),
        ('F AND B LICENSE', 'F AND B LICENSE')
    )
    GENDER_TYPES = (
        ('MALE','MALE'),
        ('FEMALE','FEMALE'),
        ('TRANSGENDER','TRANSGENDER')
    )
    id_proof_type = models.CharField(max_length=20, choices=id_proof_types)
    other_id_proof_type = models.CharField(max_length=20, choices=other_id_proof_types, blank=True, null=True)
    id_proof_type_number = models.CharField(max_length=20, null=True, blank=True, unique=True)
    id_proof_file = models.FileField(upload_to='ID_PROOF/', null=True, blank=True)
    validity = models.DateTimeField(null=True, blank=True)
    nsr = models.FileField(upload_to='PCC/', null=True, blank=True)
    pcc = models.FileField(upload_to='NSR/', null=True, blank=True)
    resume = models.FileField(upload_to='RESUME/',null=True,blank=True)
    gender = models.CharField(max_length=20,choices=GENDER_TYPES,null=True,blank=True)
    bank_details = models.FileField(upload_to='BANK/',null=True,blank=True)

    verified = models.BooleanField(default=False)

    def clean(self):
        # Convert empty strings to None for unique fields
        if self.pf_no == '':
            self.pf_no = None
        if self.employee_esi_no == '':
            self.employee_esi_no = None

        # Custom validation to ensure at least one field is filled
        if not self.id_proof_type and not self.id_proof_file:
            raise ValidationError('You must provide either an Aadhar number or upload a file.')

        if self.other_id_proof_type == "DRIVING LICENSE":
            # Example: Driving License must match a specific format
            if not re.match(r"^[A-Z]{2}\d{13}$", self.id_proof_type_number):
                raise ValidationError({
                    'id_proof_type_number': 'Driving License must follow the format: 2 uppercase letters followed by 13 digits (e.g., DL0123456789123).'
                })

        if self.other_id_proof_type == "F AND B LICENSE":
            # Example: F and B License must match a different format
            if not re.match(r"^FB-\d{10}$", self.id_proof_type_number):
                raise ValidationError({
                    'id_proof_type_number': 'F and B License must follow the format: FB- followed by 10 digits (e.g., FB-1234567890).'
                })

        if self.id_proof_type == "AADHAR":
            if not re.match(r"^\d{12}$", self.id_proof_type_number):
                raise ValidationError({
                    'id_proof_type_number': 'AADHAR CARD must follow the format: 2 uppercase letters followed by 13 digits (e.g., 596206677449).'
                })

        if self.id_proof_type == "PAN CARD":
            if not re.match(r"^[A-Z]{5}\d{4}[A-Z]{1}$", self.id_proof_type_number):
                raise ValidationError({
                    'id_proof_type_number': 'PAN CARD must follow the format: FB- followed by 10 digits (e.g., ADYPM6101D).'
                })

        if self.id_proof_type == "PASSPORT":
            if not re.match(r"^[A-Z]{1}\d{7}$", self.id_proof_type_number):
                raise ValidationError({
                    'id_proof_type_number': 'PASSPORT must follow the format: FB- followed by 10 digits (e.g., J8369854).'
                })

        # Check for duplicate ESI and PF numbers
        if self.employee_esi_no:
            existing_esi = EmployeeDetails.objects.filter(employee_esi_no=self.employee_esi_no).exclude(pk=self.pk)
            if existing_esi.exists():
                raise ValidationError({'employee_esi_no': 'This ESI number already exists.'})

        if self.pf_no:
            existing_pf = EmployeeDetails.objects.filter(pf_no=self.pf_no).exclude(pk=self.pk)
            if existing_pf.exists():
                raise ValidationError({'pf_no': 'This PF number already exists.'})

    def check_complete(self):
        # List of required fields to consider the details as complete
        required_fields = [self.basic, self.pf_no, self.employee_esi_no]
        if all(required_fields):
            self.is_complete = True
        else:
            self.is_complete = False

    def save(self, *args, **kwargs):
        # Update completeness status before saving
        self.check_complete()
        super(EmployeeDetails, self).save(*args, **kwargs)



class RequestLeave(models.Model):
    employee = models.ForeignKey(EmployeeDetails, on_delete=models.CASCADE, null=True,related_name='leaverequest')

    LEAVE_TYPE_CHOICES = (
        ('Sick Leave', 'Sick Leave'),
        ('Casual Leave', 'Casual Leave'),
        ('Paid Leave', 'Paid Leave'),
    )

    leave_type = models.CharField(max_length=100, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    reason = models.CharField(max_length=120, null=True)

    Approval_Type = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    verification_status = models.CharField(max_length=100, choices=Approval_Type, default='Pending')
    approval_status = models.CharField(max_length=100, choices=Approval_Type, default='Pending')
    rejection_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee} - {self.approval_status}"


class Payroll(models.Model):
    employee = models.ForeignKey(EmployeeDetails, on_delete=models.CASCADE)

    # Earnings
    hra = models.DecimalField(max_digits=10, decimal_places=2)
    da = models.DecimalField(max_digits=10, decimal_places=2)
    ot = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=Decimal('0.00'))
    leave_plus = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=Decimal('0.00'))

    medical = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=Decimal('0.00'))
    insurance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=Decimal('0.00'))
    ta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=Decimal('0.00'))
    food_allowance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                         default=Decimal('0.00'))

    # Deductions
    canteen_expense = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                          default=Decimal('0.00'))
    pf = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=Decimal('0.00'))
    esi = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=Decimal('0.00'))

    # Bonuses
    bonuses = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=Decimal('0.00'))

    # Computed field
    net_pay = models.DecimalField(max_digits=10, decimal_places=2)
    pay_date = models.DateField()

    def __str__(self):
        return f"{self.employee}"

class Resignation(models.Model):
    ACTIVE = 'Active'
    RESIGNED = 'Resigned'
    PENDING = 'Pending'
    APPROVED_BY_SENIOR = 'Approved by Senior'
    APPROVED_BY_HR = 'Approved by HR'

    RESIGNATION_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED_BY_SENIOR, 'Approved by Senior'),
        (APPROVED_BY_HR, 'Approved by HR'),
        (RESIGNED, 'Resigned'),
    ]
    employee = models.ForeignKey(EmployeeDetails, on_delete=models.CASCADE ,null=True)
    status = models.CharField(max_length=20, choices=RESIGNATION_STATUS_CHOICES, default=ACTIVE)
    resignation_status = models.CharField(max_length=20, choices=RESIGNATION_STATUS_CHOICES, default=PENDING)
    senior_approval = models.BooleanField(default=False)
    hr_approval = models.BooleanField(default=False)

    # Add the missing fields
    date = models.DateField(null=True)
    remarks = models.TextField(null=True, blank=True)
    reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Resignation for {self.employee.user.name} - {self.resignation_status}"

class Remarks(models.Model):
    date = models.DateField(blank=True, null=True)
    reason = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.CharField(max_length=200, null=True)
    ratings = models.IntegerField(choices=[(i, f'{i} Star') for i in range(1, 6)], null=True, blank=True)
    suggest_to_improve = models.CharField(max_length=100,null=True,blank=True)

class Attendance(models.Model):
    employee = models.ForeignKey(EmployeeDetails, on_delete=models.CASCADE)
    date = models.DateField()
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Leave', 'Leave')],
        default='Present'
    )

    def __str__(self):
        return f"{self.employee} - {self.date} - {self.status}"

    @property
    def worked_hours(self):
        if self.check_in_time and self.check_out_time:
            return (datetime.combine(date.min, self.check_out_time) - datetime.combine(date.min, self.check_in_time)).seconds // 3600
        return None

class AttendanceReport(models.Model):
    employee = models.ForeignKey(EmployeeDetails, on_delete=models.CASCADE, related_name="attendance_reports")
    report_month = models.DateField()  # Use the first day of the month to represent the month
    total_days_worked = models.PositiveIntegerField(default=0)
    total_leaves = models.PositiveIntegerField(default=0)
    total_absent = models.PositiveIntegerField(default=0)
    total_hours_worked = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.employee.user.name} - {self.report_month.strftime('%B, %Y')}"

    class Meta:
        unique_together = ("employee", "report_month")