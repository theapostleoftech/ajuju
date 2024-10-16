"""
This module contains the views for the quiz subjects.
"""
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
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
    """
    This view is used to create a new subject.
    """
    model = Subject
    form_class = SubjectForm
    template_name = 'quiz/subject_form.html'
    success_url = reverse_lazy('quiz:subject_index')

    def form_valid(self, form):
        form.instance.creator = self.request.user.teacher
        messages.success(self.request, f"Subject has been created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error creating the subject. Please try again.")
        return super().form_invalid(form)


class SubjectUpdateView(CreatorBaseUpdateView):
    """
    This is the view for updating a subject.
    """
    model = Subject
    form_class = SubjectForm
    template_name = 'quiz/subject_form.html'
    success_url = reverse_lazy('quiz:subject_index')

    def get_object(self, queryset=None):
        # Fetch the subject by UUID from the URL
        subject = get_object_or_404(Subject, id=self.kwargs['pk'])

        # Ensure the logged-in user is the creator of the subject
        if subject.creator != self.request.user.teacher:
            messages.error(self.request, f"You do not have permission to update the subject {self.object.name}.")
            return HttpResponseForbidden()
        return subject

    def form_valid(self, form):
        messages.success(self.request, f"The Subject {self.object.name} has been updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, f"There was an error updating the subject {self.object.name}. Please try again.")
        return super().form_invalid(form)


class SubjectDeleteView(CreatorBaseDeleteView):
    model = Subject
    success_url = reverse_lazy('quiz:subject_index')
    template_name = 'quiz/subject_confirm_delete.html'
