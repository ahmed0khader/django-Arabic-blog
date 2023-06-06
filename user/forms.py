from dataclasses import fields
from django import forms
from django.contrib.auth.models import User
from .models import *

class registerForm(forms.ModelForm):
    username = forms.CharField(label='اسم المستخدم', max_length=50, help_text='يجب الا يحتوي اسم المستخدم على (مسافة * _ - # @ )')
    email = forms.CharField(label='البريد الالكتروني', max_length=50)
    first_name = forms.CharField(label='الاسم الاول', max_length=30)
    last_name = forms.CharField(label='الاسم الثاني', max_length=30)
    password1 = forms.CharField(label='كلمة المرور', widget=forms.PasswordInput(), min_length=8,  help_text='يجب ان لا تقل عن 8 مدخلات وان تحتوي على احرف')
    password2 = forms.CharField(label='تاكيد كلمة المرور', widget=forms.PasswordInput(), min_length=8)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        ]
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('كلمة المرور غير متطابقة')
            
        return cd['password2']

    def clean_username(self):
        cd = self.cleaned_data
        if User.objects.filter(username=cd['username']).exists():
            raise forms.ValidationError('هذا الاسم مستخدم')
        return cd['username']

class LoginForms(forms.ModelForm):
    username = forms.CharField(label='اسم المستخدم')
    password = forms.CharField(label='كلمة المرور', widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='الاسم الاول', max_length=30)
    last_name = forms.CharField(label='الاسم الثاني', max_length=30)
    email = forms.CharField(label='البريد الالكتروني', max_length=50)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)