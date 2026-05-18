from django import forms
from django.contrib.auth.models import User
from .models import EmployeeProfile, Department


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ['middle_name', 'department', 'job_title', 'phone', 'mobile', 'location', 'bio', 'avatar', 'is_manager']
        widgets = {
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (000) 000-00-00'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (000) 000-00-00'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Office / City'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'is_manager': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }