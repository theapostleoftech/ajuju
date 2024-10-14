"""
This module contains the form for OTP (One-Time Password) verification.
"""
from django import forms

from core.forms import BaseFormMixin


class OTPVerificationForm(BaseFormMixin, forms.Form):
    """
    Form for OTP (One-Time Password) verification.
    """

    otp = forms.CharField(
        label='OTP',
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={'autofocus': True}),
        help_text="Enter the 6-digit OTP sent to your email, SMS, or WhatsApp."
    )

    def clean_otp(self):
        """
        Clean and validate the OTP field.
        This method ensures that the OTP consists of exactly 6 digits.
        """
        otp = self.cleaned_data['otp']
        if not otp.isdigit() or len(otp) != 6:
            raise forms.ValidationError("OTP must be 6 digits.")
        return otp
