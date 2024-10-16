"""
This file contains the form for the Subject model.
"""
from django import forms

from core.forms import BaseFormMixin
from quiz.models import Subject


class SubjectForm(BaseFormMixin, forms.ModelForm):
    """
    This form is used to create and update subjects.
    """

    class Meta:
        model = Subject
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
