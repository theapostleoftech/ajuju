from django import forms
from django.forms import modelformset_factory

from core.forms import BaseFormMixin
from quiz.models import Choice, Question, Quiz, QuizAttempt


class QuizForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'subject', 'time_limit']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class QuestionForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', ]


class ChoiceForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']


class QuizAttemptForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = QuizAttempt
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['confirm'] = forms.BooleanField(
            required=True,
            label="I'm ready to start the quiz",
            widget=forms.CheckboxInput(attrs={'class': 'form-check-input rounded-full'})
        )


QuestionFormSet = modelformset_factory(Question, fields=['text'], extra=1)
ChoiceFormSet = modelformset_factory(Choice, fields=['text', 'is_correct'], extra=1)
