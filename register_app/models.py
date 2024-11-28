from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator, EmailValidator



# Create your models here.
class department(models.Model):
    USER_TYPE_CHOICES = (
        ('BOD', 'BOD'),
        ('Admin', 'Admin'),
        ('Sales', 'Sales'),
        ('Purchase', 'Purchase'),
        ('Inventory', 'Inventory'),
        ('Logistics', 'Logistics'),
        ('Production', 'Production'),
        ('R & D', 'R & D'),
        ('HR', 'HR'),
        ('Accounts', 'Accounts'),
    )
    dept_Name = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.dept_Name


class designation(models.Model):

    user_type = models.CharField(max_length=100,)
    dept = models.ForeignKey(department, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user_type} - {self.dept}"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator(message="Enter a valid email address.")],
    )
    phone_number = models.CharField(
        max_length=10,  # Set max_length to 10 for a 10-digit number
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',  # Matches exactly 10 digits
                message="Enter a valid 10-digit phone number."
            )
        ],
    )
    designation = models.ForeignKey('designation', on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey('department', on_delete=models.CASCADE, null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Admin status
    is_superuser = models.BooleanField(default=False)  # Superuser status
    image = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    unique_id = models.CharField(max_length=100, null=True, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()



    def __str__(self):
        if self.name:
            return f"{self.name} ({self.email}) - ID: {self.unique_id}"
        return f"{self.email} - ID: {self.unique_id}"


class MenuPermissions(models.Model):
    user = models.ForeignKey('register_app.CustomUser', on_delete=models.CASCADE, null=True)  # Use the correct app name
    menu = models.ForeignKey('Glenda_App.Menu', on_delete=models.CASCADE, null=True, blank=True)  # Optional association with Menu
    sub_menu = models.ForeignKey('Glenda_App.SubMenu', on_delete=models.CASCADE, null=True,blank=True)  # Optional association with SubMenu

    def __str__(self):
        return f"Permissions for {self.user} - Menu: {self.menu}, SubMenu: {self.sub_menu}"

    class Meta:
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"
