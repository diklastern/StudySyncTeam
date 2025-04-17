from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from datetime import date
from .constants import UNIVERSITIES, DEGREE_PROGRAMS, STUDY_YEARS

DAYS_OF_WEEK = [
    ('sun', 'Sunday'),
    ('mon', 'Monday'),
    ('tue', 'Tuesday'),
    ('wed', 'Wednesday'),
    ('thu', 'Thursday'),
    ('fri', 'Friday'),
    ('sat', 'Saturday'),
]

class CustomUser(AbstractUser):
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    university = models.CharField(max_length=50, choices=UNIVERSITIES)
    degree_program = models.CharField(max_length=50, choices=DEGREE_PROGRAMS)
    year_of_study = models.PositiveSmallIntegerField(choices=STUDY_YEARS)

    def __str__(self):
        return f"{self.full_name} ({self.get_degree_program_display()})"


class SoloAvailability(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    week_start = models.DateField(help_text="Sunday of the week")
    day = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('user', 'week_start', 'day', 'start_time')
        ordering = ['week_start', 'day', 'start_time']

    def __str__(self):
        return f"{self.user.username} SOLO {self.week_start} {self.day} {self.start_time}-{self.end_time}"

class GroupAvailability(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    week_start = models.DateField(help_text="Sunday of the week")
    day = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('user', 'week_start', 'day', 'start_time')
        ordering = ['week_start', 'day', 'start_time']

    def __str__(self):
        return f"{self.user.username} GROUP {self.week_start} {self.day} {self.start_time}-{self.end_time}"