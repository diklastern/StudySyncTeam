from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .constants import UNIVERSITIES, DEGREE_PROGRAMS, STUDY_YEARS

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'full_name', 'university', 'degree_program', 'year_of_study']
        widgets = {
            'university': forms.Select(choices=UNIVERSITIES),
            'degree_program': forms.Select(choices=DEGREE_PROGRAMS),
            'year_of_study': forms.Select(choices=STUDY_YEARS),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input'

class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'university', 'degree_program', 'year_of_study']
        widgets = {
            'university': forms.Select(choices=UNIVERSITIES),
            'degree_program': forms.Select(choices=DEGREE_PROGRAMS),
            'year_of_study': forms.Select(choices=STUDY_YEARS),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input'