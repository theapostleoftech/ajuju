class BaseFormMixin:
    """
    A mixin that updates form field widgets with a set of default HTML attributes.
    Allows for customization of the CSS classes and other widget attributes.
    """

    def __init__(self, *args, **kwargs):
        # Optional: Allow custom widget attributes to be passed in via kwargs
        self.widget_attrs = kwargs.pop('widget_attrs', {
            'class': 'inset-y-0 disabled:opacity-50 disabled:pointer-events-none rounded-xl text-sm '
                     'inline-flex focus:border-accent-800 focus:ring-accent-800 bg-light-500 '
                     'appearance-none w-full ps-10 p-3 py-3.5 px-4 border border-accent-300'
        })

        super().__init__(*args, **kwargs)
        self.apply_widget_attrs()

    def apply_widget_attrs(self):
        """
        Applies the defined widget attributes to all fields in the form.
        """
        for field_name, field in self.fields.items():
            if field.widget:
                # Update the widget's attributes
                field.widget.attrs.update(self.widget_attrs)
                # Optionally: Customize attributes per field here if needed
                field.widget.attrs.update({'placeholder': f'Enter {field.label}'})