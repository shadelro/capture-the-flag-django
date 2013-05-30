# -*- coding: utf-8 -*-

import hashlib

from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    login_username = forms.CharField(min_length=1, max_length=75, 
                                     label='Username', 
                                     widget=forms.TextInput(attrs={'size':'30'}))
    login_password = forms.CharField(min_length=1, max_length=40, 
                                     label='Password', 
                                     widget=forms.PasswordInput(attrs={'size':'30','autocomplete':'off'}, render_value=False))
    next = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = self.cleaned_data            
        username = cleaned_data.get('login_username')        
        password = cleaned_data.get('login_password')
        if username and password:
            # In case the user accidently puts spaces before/after...
            username = username.strip()
        return cleaned_data
    
    def is_valid(self):
        return super(LoginForm, self).is_valid() and not (hasattr(self, 'error_msg') and self.error_msg)


class SignupForm(forms.Form):
    signup_username = forms.CharField(min_length=1, max_length=75, 
                                     label='Username', 
                                     widget=forms.TextInput(attrs={'size':'30'}))
    signup_password = forms.CharField(min_length=1, max_length=40, 
                                     label='Password', 
                                     widget=forms.PasswordInput(attrs={'size':'30','autocomplete':'off'}, render_value=False))
    next = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = self.cleaned_data            
        username = cleaned_data.get('signup_username')        
        password = cleaned_data.get('signup_password')
        if username and password:
            username = username.strip()
            hashed_password = hashlib.md5(password).hexdigest()
            User.objects.get_or_create(username=username, defaults={'password': hashed_password, 'is_active': True})
            #User.objects.get_or_create(username=username, defaults={'password': password, 'is_active': True})
            
        return cleaned_data
    
    def is_valid(self):
        return super(SignupForm, self).is_valid() and not (hasattr(self, 'error_msg') and self.error_msg)
