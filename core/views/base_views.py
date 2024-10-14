"""
This module contains the base views for the ajuju app.
"""

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, ListView, DeleteView

from ajuju.utils.decorators import whizzer_required, creator_required


@method_decorator([login_required, whizzer_required])
class WhizzerBaseCreateView(CreateView):
    """
    This is the base view for creating a whizzer object.
    """

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@method_decorator([login_required, whizzer_required])
class WhizzerBaseUpdateView(UpdateView):
    """
    This is the base view for updating a whizzer object.
    """

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@method_decorator([login_required, whizzer_required])
class WhizzerBaseListView(ListView):
    """
    This is the base view for listing whizzer objects.
    """

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@method_decorator([login_required, whizzer_required])
class WhizzerBaseDeleteView(DeleteView):
    """

    """

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@method_decorator([login_required, creator_required])
class CreatorBaseCreateView(CreateView):
    """
    This is the base view for creating a creator object.
    """

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@method_decorator([login_required, creator_required])
class CreatorBaseUpdateView(UpdateView):
    """
    This is the base view for updating a creator object.
    """

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@method_decorator([login_required, creator_required])
class CreatorBaseListView(ListView):
    """
    This is the base view for listing a creator object
    """

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@method_decorator([login_required, creator_required])
class CreatorBaseDeleteView(DeleteView):
    """
    This is the base view for deleting a creator object
    """

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
