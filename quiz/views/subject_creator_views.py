"""
This module contains the views for the quiz subjects.
"""
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from core.views.base_views import CreatorBaseCreateView, CreatorBaseUpdateView, CreatorBaseDeleteView
from ..forms.subject_forms import SubjectForm
from ..models import Subject


class SubjectListView(ListView):
    model = Subject
    template_name = 'quiz/subject_list.html'
    context_object_name = 'subjects'


class SubjectDetailView(DetailView):
    model = Subject
    template_name = 'quiz/subject_detail.html'


class SubjectCreateView(CreatorBaseCreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'quiz/subject_form.html'
    success_url = reverse_lazy('subject_list')


class SubjectUpdateView(CreatorBaseUpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'quiz/subject_form.html'
    success_url = reverse_lazy('subject_list')


class SubjectDeleteView(CreatorBaseDeleteView):
    model = Subject
    success_url = reverse_lazy('subject_list')
    template_name = 'quiz/subject_confirm_delete.html'
