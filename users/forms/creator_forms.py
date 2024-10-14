"""
This module contains the forms for the Creator model.
"""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from core.forms import BaseFormMixin


class CreatorSignUpEmailForm(BaseFormMixin, forms.ModelForm):
    """
    This is the sign up form for the email details of a Creator.
    """

    class Meta:
        model = get_user_model()
        fields = ['email', 'username']

    def clean_email(self):
        """
        Clean and validate the email field.
        :return:
        """
        email = self.cleaned_data['email']
        existing_user = get_user_model().objects.filter(email=email).first()
        if existing_user:
            if existing_user.is_active and existing_user.is_email_verified:
                raise forms.ValidationError("An account with this email already exists. Please log in instead.")
        return email

    def clean_username(self):
        """
        Clean and validate the username field.
        :return:
        """
        username = self.cleaned_data['username']
        existing_user = get_user_model().objects.filter(username=username).first()
        if existing_user:
            if existing_user.is_active and existing_user.is_email_verified:
                raise forms.ValidationError("An account with this username already exists. Please log in instead.")
        return username


class CreatorSignUpPersonalDetailForm(BaseFormMixin, forms.ModelForm):
    """
    This is the sign up form for the personal details of a Creator.
    """

    class Meta:
        model = get_user_model()
        fields = ['full_name']


class CreatorSignUpPasswordForm(BaseFormMixin, UserCreationForm):
    """
       This is the sign up form for the password details of a Creator.
    """

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("password1", "password2")
