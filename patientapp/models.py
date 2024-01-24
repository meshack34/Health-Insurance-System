from datetime import datetime
from django.db import models
from datetime import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import date
from datetime import datetime
from django.db.models.deletion import CASCADE
from django.db.models.enums import Choices
from django.shortcuts import redirect
from multiselectfield import MultiSelectField
from django.db import models
from django.contrib.auth.models import  AbstractBaseUser , BaseUserManager, PermissionsMixin
from django.db import models

class Card(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    caption = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class AccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, first_name, last_name, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user



class Account(AbstractBaseUser):
    email           = models.EmailField(max_length=100, unique=True)
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    username        = models.CharField(max_length=50, unique=True)
    phone_number    = models.CharField(max_length=50)
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=True)
    is_superadmin        = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = AccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class Customer(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    profile_image = models.ImageField(upload_to='customer/%Y/%m/%d/', default='default.png')
    city = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)
    blood_group = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(Account, on_delete=models.DO_NOTHING, null=True)
    date_joined = models.DateTimeField(default=date.today, blank=True)
    date_of_birth = models.DateField(null=True)
    age_years = models.PositiveIntegerField(null=True)  

    @property
    def calculate_age(self):  
        today = date.today()
        if self.date_of_birth:
            age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            return age
        return None
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

class Claim(models.Model):
    claimant = models.ForeignKey('Customer', on_delete=models.CASCADE)
    claim_details = models.TextField()
    claim_status = models.CharField(max_length=50)

    def __str__(self):
        return f"Claim #{self.pk} - {self.claimant}"

class Policy(models.Model):
    policy_holder = models.ForeignKey('Customer', on_delete=models.CASCADE)
    policy_details = models.TextField()
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Policy #{self.pk} - {self.policy_holder}"

class Billing(models.Model):
    policy = models.ForeignKey('Policy', on_delete=models.CASCADE)
    billing_amount = models.DecimalField(max_digits=10, decimal_places=2)
    billing_date = models.DateField()

    def __str__(self):
        return f"Billing #{self.pk} - {self.policy}"

class Document(models.Model):
    document_type = models.CharField(max_length=50)
    policy = models.ForeignKey('Policy', on_delete=models.CASCADE, blank=True, null=True)
    claim = models.ForeignKey('Claim', on_delete=models.CASCADE, blank=True, null=True)
    document_file = models.FileField(upload_to='documents/')
    upload_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.document_type} - {self.upload_date}"

