from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from datetime import date
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from .constants import UNIVERSITIES, DEGREE_PROGRAMS, STUDY_YEARS, DAYS_OF_WEEK


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('username', None)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('username', None)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(max_length=100)
    university = models.CharField(max_length=100, choices=UNIVERSITIES)
    degree_program = models.CharField(max_length=100, choices=DEGREE_PROGRAMS)
    year_of_study = models.SmallIntegerField(choices=STUDY_YEARS, default=1)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    
   

    def __str__(self):
        return self.email
    
    