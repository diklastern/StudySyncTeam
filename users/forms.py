from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser
from .constants import UNIVERSITIES, DEGREE_PROGRAMS, STUDY_YEARS


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
    )

    class Meta:
        model = CustomUser
        fields = [
            'email', 'password1', 'password2',
            'full_name', 'university', 'degree_program',
            'year_of_study', 'image'
        ]
        widgets = {
            'university': forms.Select(choices=UNIVERSITIES),
            'degree_program': forms.Select(choices=DEGREE_PROGRAMS),
            'year_of_study': forms.Select(choices=STUDY_YEARS),
        }

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input'

class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'image', 'full_name', 'university',
            'degree_program', 'year_of_study'
        ]
        widgets = {
            'university': forms.Select(choices=UNIVERSITIES),
            'degree_program': forms.Select(choices=DEGREE_PROGRAMS),
            'year_of_study': forms.Select(choices=STUDY_YEARS),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input'



class EmailLoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'input is-rounded',
            'placeholder': 'Enter your email',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'input is-rounded',
            'placeholder': 'Enter your password'
        })
    )