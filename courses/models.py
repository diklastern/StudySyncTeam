from django.db import models
from django.conf import settings
from users.constants import UNIVERSITIES, STUDY_YEARS

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    university = models.CharField(max_length=100, choices=UNIVERSITIES)
    year = models.PositiveSmallIntegerField(choices=STUDY_YEARS)

    def __str__(self):
        return f"{self.code} - {self.name} ({self.get_university_display()})"



class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.name}"
