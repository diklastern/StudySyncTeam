# Updated models.py (app: users or availability)
from django.db import models
from django.conf import settings
from users.constants import DAYS_OF_WEEK

class AvailabilityBase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    week_start = models.DateField(help_text="Sunday of the week")
    day = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    repeated = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ['week_start', 'day', 'start_time']

    def duration_hours(self):
        return (datetime.combine(date.today(), self.end_time) - datetime.combine(date.today(), self.start_time)).seconds / 3600

    def __str__(self):
        return f"{self.user.email} {self.__class__.__name__.replace('Availability', '')} {self.week_start} {self.day} {self.start_time}-{self.end_time}"

class SoloAvailability(AvailabilityBase):
    class Meta(AvailabilityBase.Meta):
        unique_together = ('user', 'week_start', 'day', 'start_time')

class GroupAvailability(AvailabilityBase):
    class Meta(AvailabilityBase.Meta):
        unique_together = ('user', 'week_start', 'day', 'start_time')