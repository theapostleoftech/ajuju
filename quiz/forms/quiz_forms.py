from django import forms

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
        fields = ['text', 'order']


class ChoiceForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']


class QuizAttemptForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = QuizAttempt
        fields = []  # We don't need any fields, as we'll set them programmatically

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['confirm'] = forms.BooleanField(
            required=True,
            label="I'm ready to start the quiz",
            widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
        )


ChoiceFormSet = forms.inlineformset_factory(
    Question, Choice, form=ChoiceForm, extra=4, can_delete=True, min_num=2, validate_min=True
)

QuestionFormSet = forms.inlineformset_factory(
    Quiz, Question, form=QuestionForm, extra=1, can_delete=True
)
