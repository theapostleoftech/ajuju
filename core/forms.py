class BaseFormMixin:
    """
    A mixin that updates form field widgets with a set of default HTML attributes.
    Allows for customization of the CSS classes and other widget attributes.
    """

    def __init__(self, *args, **kwargs):
        self.widget_attrs = kwargs.pop('widget_attrs', {
            'class': "block py-2.5 px-0 w-full text-sm text-accent-900 bg-transparent border-0 border-b-2 border-accent-300 appearance-none focus:outline-none focus:ring-0 focus:border-accent-600 peer"
        })

        super().__init__(*args, **kwargs)
        self.apply_widget_attrs()

    def apply_widget_attrs(self):
        """
        Applies the defined widget attributes to all fields in the form.
        """
        for field_name, field in self.fields.items():
            if field.widget:
                field.widget.attrs.update(self.widget_attrs)
                field.widget.attrs.update({'placeholder': f'Enter {field.label}'})
