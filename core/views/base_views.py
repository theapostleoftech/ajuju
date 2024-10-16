"""
This module contains the base views for the ajuju app.
"""

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, TemplateView

from ajuju.utils.decorators import whizzer_required, creator_required


@method_decorator([login_required, whizzer_required], name='dispatch')
class WhizzerBaseTemplateView(TemplateView):
    """
    This is the base view for updating a whizzer object.
    """

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@method_decorator([login_required, whizzer_required], name='dispatch')
class WhizzerBaseCreateView(CreateView):
    """
    This is the base view for creating a whizzer object.
    """

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@method_decorator([login_required, whizzer_required], name='dispatch')
class WhizzerBaseUpdateView(UpdateView):
    """
    This is the base view for updating a whizzer object.
    """

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@method_decorator([login_required, whizzer_required], name='dispatch')
class WhizzerBaseListView(ListView):
    """
    This is the base view for listing whizzer objects.
    """

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@method_decorator([login_required, whizzer_required], name='dispatch')
class WhizzerBaseDeleteView(DeleteView):
    """
    This is the base view for deleting a whizzer object.
    """

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@method_decorator([login_required, creator_required], name='dispatch')
class CreatorBaseTemplateView(TemplateView):
    """
    This is the base view for deleting a creator object
    """

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@method_decorator([login_required, creator_required], name='dispatch')
class CreatorBaseCreateView(CreateView):
    """
    This is the base view for creating a creator object.
    """

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@method_decorator([login_required, creator_required], name='dispatch')
class CreatorBaseUpdateView(UpdateView):
    """
    This is the base view for updating a creator object.
    """

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@method_decorator([login_required, creator_required], name='dispatch')
class CreatorBaseListView(ListView):
    """
    This is the base view for listing a creator object
    """

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@method_decorator([login_required, creator_required], name='dispatch')
class CreatorBaseDeleteView(DeleteView):
    """
    This is the base view for deleting a creator object
    """

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
