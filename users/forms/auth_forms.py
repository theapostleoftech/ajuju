"""
This module contains the form for the login process.
"""
from django import forms

from core.forms import BaseFormMixin


class LoginForm(BaseFormMixin, forms.Form):
    """
    Form for the login process.
    """
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput
    )
