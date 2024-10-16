from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, SetPasswordForm

from core.forms import BaseFormMixin
from users.models import UserModel


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all required fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'full_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all fields on the user, but replaces
    the password field with admin's password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'full_name', 'password', 'is_active', 'is_staff', 'is_superuser')

    def clean_password(self):
        return self.initial["password"]


class UserAccountUpdateForm(BaseFormMixin, forms.ModelForm):
    """
    This form is used to update the user account details.
    """
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'full_name',)

    def __init__(self, *args, **kwargs):
        super(UserAccountUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['email'].disabled = True



class ChangePasswordForm(BaseFormMixin, SetPasswordForm):
    """
    This is used to change the user password
    """
    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(),
        required=True
    )

    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(),
        required=True
    )

    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(),
        required=True
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Sorry, your old password is incorrect.")
        return old_password

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
