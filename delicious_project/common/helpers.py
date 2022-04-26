class DisabledFieldsFormMixin:
    fields = {}
    def _init_disabled_fields(self):
        for _, field in self.fields.items():
            if not hasattr(field.widget, 'attrs'):
                setattr(field.widget, 'attrs', {})
            field.widget.attrs['disabled'] = 'disabled'
            field.required = False