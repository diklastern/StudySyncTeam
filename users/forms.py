from django import forms
from .models import UserProfile
from .constants import UNIVERSITIES, DEGREE_PROGRAMS, STUDY_YEARS

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'university', 'degree_program', 'year_of_study']
        widgets = {
            'university': forms.Select(choices=UNIVERSITIES),
            'degree_program': forms.Select(choices=DEGREE_PROGRAMS),
            'year_of_study': forms.Select(choices=STUDY_YEARS),
        }