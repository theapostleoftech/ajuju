from django.views.generic import TemplateView


# Create your views here.
class IndexView(TemplateView):
    """
    This is the view for the index page.
    """
    template_name = 'core/index.html'
